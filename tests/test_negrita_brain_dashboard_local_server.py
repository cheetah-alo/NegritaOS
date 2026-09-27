"""Unit tests for the local-only NegritaOS 360 HTTP bridge."""

from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from negrita_brain.dashboard_local_server import create_local_server, main


class _FakeServer:
    def __init__(self, address, handler_class) -> None:
        self.bound_address = address
        self.RequestHandlerClass = handler_class
        self.server_port = 8791

    def server_close(self) -> None:
        pass


class _MemorySocket:
    def __init__(self, request: bytes) -> None:
        self.reader = io.BytesIO(request)
        self.writer = io.BytesIO()

    def makefile(self, mode: str, *args):
        return self.reader if "r" in mode else self.writer

    def sendall(self, data: bytes) -> None:
        self.writer.write(data)

    def close(self) -> None:
        pass


class TestDashboardLocalServer(unittest.TestCase):
    """Verify local binding, request boundaries, and static safety."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        (self.root / "projects").mkdir()
        self.prototype = self.root / "prototypes" / "negritaos360"
        self.prototype.mkdir(parents=True)
        (self.prototype / "index.html").write_text("<h1>ok</h1>", encoding="utf-8")
        (self.prototype / "module.mjs").write_text("export {};", encoding="utf-8")
        self.access = self.root / "access.json"
        self.access.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "project_client_grants": [],
                    "unknown_client_projects": [],
                }
            ),
            encoding="utf-8",
        )
        os.chmod(self.access, 0o600)
        self.server_constructor = patch(
            "negrita_brain.dashboard_local_server._LocalHTTPServer",
            side_effect=_FakeServer,
        )
        self.server_constructor.start()
        self.addCleanup(self.server_constructor.stop)
        self.server = create_local_server(self.root, self.access, 0)
        self.addCleanup(self.server.server_close)

    def _request(
        self, path: str, host: str | None = None, origin: str | None = None,
        method: str = "GET",
    ):
        headers = {"Host": host or f"127.0.0.1:{self.server.server_port}"}
        if origin is not None:
            headers["Origin"] = origin
        header_bytes = b"".join(
            f"{key}: {value}\r\n".encode() for key, value in headers.items()
        )
        request = f"{method} {path} HTTP/1.0\r\n".encode() + header_bytes + b"\r\n"
        socket = _MemorySocket(request)
        self.server.RequestHandlerClass(socket, ("127.0.0.1", 12345), self.server)
        raw = socket.writer.getvalue()
        head, body = raw.split(b"\r\n\r\n", 1)
        lines = head.split(b"\r\n")
        status = int(lines[0].split()[1])
        headers = [tuple(item.decode().split(": ", 1)) for item in lines[1:]]
        return status, headers, body

    def test_server_that_binds_literal_loopback_when_factory_is_created(self) -> None:
        self.assertEqual(self.server.bound_address, ("127.0.0.1", 0))
        self.assertEqual(self.server.server_port, 8791)

    def test_catalog_that_returns_versioned_json_when_policy_is_missing(self) -> None:
        self.access.unlink()
        status, headers, body = self._request("/api/v1/catalog")
        self.assertEqual(status, 200)
        self.assertEqual(dict(headers)["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(json.loads(body)["state"], "EMPTY")

    def test_capabilities_that_return_empty_without_policy_or_global_scan(self) -> None:
        self.access.unlink()
        status, _, body = self._request("/api/v1/capabilities")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["items"], [])

    def test_capabilities_that_return_scoped_items_and_filters(self) -> None:
        self.access.write_text(json.dumps({
            "schema_version": 1,
            "project_client_grants": [],
            "unknown_client_projects": ["alpha"],
        }), encoding="utf-8")
        (self.root / "projects" / "alpha.yaml").write_text(
            "project:\n  id: alpha\n  name: Alpha\n"
            "  agents: [agent_a]\n  skill_profiles: [base]\n",
            encoding="utf-8",
        )
        (self.root / "skills").mkdir()
        (self.root / "skills" / "catalog.yaml").write_text(
            "defaults: {profiles: []}\nprofiles: {base: {skills: [skill_a]}}\n"
            "skills: [{id: skill_a}]\n",
            encoding="utf-8",
        )
        (self.root / "integrator.yaml").write_text(
            "negrita_os:\n  agents: {agent_a: {}}\n"
            "  global_rules: [rules/global/global_rules.yaml]\n",
            encoding="utf-8",
        )
        status, _, body = self._request("/api/v1/capabilities?project_id=alpha&kind=skill")
        payload = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual([(item["kind"], item["id"]) for item in payload["items"]], [("skill", "skill_a")])
        self.assertEqual(set(payload["provenance"]), {"snapshot_id", "view_sha256"})

    def test_capabilities_that_reject_invalid_filters_as_json_400(self) -> None:
        status, _, body = self._request("/api/v1/capabilities?kind=used")
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body), {"error": {"code": "INVALID_REQUEST"}})

    def test_capabilities_that_return_json_503_when_global_catalog_is_malformed(self) -> None:
        self.access.write_text(json.dumps({
            "schema_version": 1,
            "project_client_grants": [],
            "unknown_client_projects": ["alpha"],
        }), encoding="utf-8")
        (self.root / "projects" / "alpha.yaml").write_text(
            "project:\n  id: alpha\n  name: Alpha\n", encoding="utf-8"
        )
        (self.root / "skills").mkdir()
        (self.root / "skills" / "catalog.yaml").write_text(
            "profiles: [unterminated", encoding="utf-8"
        )
        status, _, body = self._request("/api/v1/capabilities")
        self.assertEqual(status, 503)
        self.assertEqual(json.loads(body), {"error": {"code": "UNAVAILABLE"}})

    def test_catalog_that_rejects_unknown_or_duplicate_query_parameters(self) -> None:
        status, _, body = self._request("/api/v1/catalog?other=x")
        self.assertEqual(status, 400)
        self.assertEqual(json.loads(body), {"error": {"code": "INVALID_REQUEST"}})

    def test_catalog_that_returns_unavailable_without_policy_details_when_service_fails(self) -> None:
        self.access.write_text("not json", encoding="utf-8")
        status, _, body = self._request("/api/v1/catalog")
        self.assertEqual(status, 503)
        self.assertEqual(json.loads(body), {"error": {"code": "UNAVAILABLE"}})

    def test_request_that_rejects_host_and_origin_outside_exact_loopback_origin(self) -> None:
        status, _, _ = self._request("/", host="localhost")
        self.assertEqual(status, 400)
        status, _, _ = self._request(
            "/", origin=f"http://localhost:{self.server.server_port}"
        )
        self.assertEqual(status, 400)

    def test_static_file_that_serves_mjs_with_javascript_mime_type(self) -> None:
        status, headers, body = self._request("/module.mjs")
        self.assertEqual(status, 200)
        self.assertEqual(dict(headers)["Content-Type"], "application/javascript; charset=utf-8")
        self.assertEqual(body, b"export {};")

    def test_home_that_accepts_only_local_source_selector_query(self) -> None:
        status, _, body = self._request("/?source=local")
        self.assertEqual(status, 200)
        self.assertEqual(body, b"<h1>ok</h1>")
        invalid_status, _, _ = self._request("/?other=x")
        self.assertEqual(invalid_status, 400)

    def test_malformed_absolute_url_returns_generic_json_error(self) -> None:
        status, headers, body = self._request("http://[::1")
        self.assertEqual(status, 400)
        self.assertEqual(dict(headers)["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(json.loads(body), {"error": {"code": "INVALID_REQUEST"}})

    def test_unsupported_method_returns_generic_json_error(self) -> None:
        status, headers, body = self._request("/api/v1/catalog", method="POST")
        self.assertEqual(status, 405)
        self.assertEqual(dict(headers)["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(json.loads(body), {"error": {"code": "INVALID_REQUEST"}})

    def test_head_method_returns_headers_without_body(self) -> None:
        status, headers, body = self._request("/api/v1/catalog", method="HEAD")
        self.assertEqual(status, 405)
        self.assertEqual(dict(headers)["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(body, b"")

    def test_response_that_sets_local_security_headers_without_cors(self) -> None:
        status, headers, _ = self._request("/")
        values = dict(headers)
        self.assertEqual(status, 200)
        self.assertEqual(values["Cache-Control"], "no-store")
        self.assertNotIn("Access-Control-Allow-Origin", values)

    def test_static_path_that_rejects_traversal_dotfiles_and_unsupported_types(self) -> None:
        (self.root / "secret.txt").write_text("secret", encoding="utf-8")
        (self.prototype / ".hidden.css").write_text("body{}", encoding="utf-8")
        for path in ("/../secret.txt", "/.hidden.css", "/secret.txt"):
            status, _, _ = self._request(path)
            self.assertEqual(status, 404)

    def test_static_path_that_rejects_symlinked_files(self) -> None:
        outside = self.root / "outside.css"
        outside.write_text("body{}", encoding="utf-8")
        try:
            (self.prototype / "linked.css").symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are unavailable")
        status, _, _ = self._request("/linked.css")
        self.assertEqual(status, 404)

    def test_cli_that_rejects_port_zero(self) -> None:
        with patch("sys.stderr") as stderr:
            with self.assertRaises(SystemExit) as raised:
                main(["--port", "0"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("between 1 and 65535", stderr.write.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
