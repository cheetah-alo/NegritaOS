"""Local-only HTTP bridge for the NegritaOS 360 prototype."""

from __future__ import annotations

import argparse
import json
import os
import stat
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

from .dashboard_local_service import LocalCatalogError, LocalCatalogService


_SUPPORTED_TYPES = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".ttf": "font/ttf",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
}
_CSP = (
    "default-src 'self'; script-src 'self'; connect-src 'self'; font-src 'self'; "
    "img-src 'self'; style-src 'self' 'unsafe-inline'"
)


class _LocalHTTPServer(ThreadingHTTPServer):
    """Threaded server with no access logging or externally visible errors."""

    daemon_threads = True
    allow_reuse_address = False


def create_local_server(
    work_root: Path, access_path: Path, port: int = 8791
) -> ThreadingHTTPServer:
    """Create a loopback-only local bridge without reading the catalog.

    Args:
        work_root: Repository root containing ``projects`` and ``prototypes``.
        access_path: Local dashboard access policy path.
        port: TCP port; ``0`` is accepted for test-assigned ephemeral ports.

    Returns:
        A server bound literally to ``127.0.0.1``.
    """
    if not isinstance(work_root, Path) or not isinstance(access_path, Path):
        raise ValueError("work_root and access_path must be pathlib.Path values")
    if type(port) is not int or not 0 <= port <= 65535:
        raise ValueError("port must be between 0 and 65535")

    service = LocalCatalogService(work_root, access_path)
    static_root = work_root / "prototypes" / "negritaos360"
    handler = _make_handler(service, static_root)
    return _LocalHTTPServer(("127.0.0.1", port), handler)


def _make_handler(
    service: LocalCatalogService, static_root: Path
) -> type[BaseHTTPRequestHandler]:
    class LocalHandler(BaseHTTPRequestHandler):
        """Serve only the versioned API and the local prototype."""

        server_version = "NegritaOS360"
        sys_version = ""

        def log_message(self, format: str, *args: object) -> None:
            """Suppress query, path, policy, and client information in logs."""

        def do_GET(self) -> None:  # noqa: N802 - required HTTP handler API
            if not self._valid_origin_headers():
                self._send_error(HTTPStatus.BAD_REQUEST, "INVALID_REQUEST")
                return
            try:
                parsed = urlsplit(self.path)
            except (ValueError, UnicodeError):
                self._send_error(HTTPStatus.BAD_REQUEST, "INVALID_REQUEST")
                return
            if parsed.path == "/api/v1/catalog":
                self._serve_catalog(parsed.query)
                return
            if parsed.path == "/" or parsed.path.startswith("/"):
                self._serve_static(parsed)
                return
            self._send_error(HTTPStatus.NOT_FOUND, "INVALID_REQUEST")

        def send_error(
            self, code: int, message: str | None = None, explain: str | None = None
        ) -> None:
            """Keep base-handler parse and unsupported-method errors in JSON."""
            try:
                status = HTTPStatus(code)
            except ValueError:
                status = HTTPStatus.BAD_REQUEST
            if status is HTTPStatus.NOT_IMPLEMENTED:
                status = HTTPStatus.METHOD_NOT_ALLOWED
            self._send_error(status, "INVALID_REQUEST")

        def _valid_origin_headers(self) -> bool:
            expected_host = f"127.0.0.1:{self.server.server_port}"
            if self.headers.get("Host") != expected_host:
                return False
            origin = self.headers.get("Origin")
            return origin is None or origin == f"http://{expected_host}"

        def _serve_catalog(self, query: str) -> None:
            try:
                params = parse_qs(query, keep_blank_values=True, strict_parsing=True)
                if set(params) - {"project_id", "client_id"}:
                    raise ValueError
                if any(len(values) != 1 for values in params.values()):
                    raise ValueError
                project_id = _single_param(params, "project_id")
                client_id = _single_param(params, "client_id")
                payload = service.read_catalog(project_id, client_id).to_dict()
            except (LocalCatalogError, OSError):
                self._send_error(HTTPStatus.SERVICE_UNAVAILABLE, "UNAVAILABLE")
                return
            except (ValueError, UnicodeError):
                self._send_error(HTTPStatus.BAD_REQUEST, "INVALID_REQUEST")
                return
            self._send_json(HTTPStatus.OK, payload)

        def _serve_static(self, parsed: Any) -> None:
            if parsed.query and not (
                parsed.path in {"/", "/index.html"} and parsed.query == "source=local"
            ):
                self._send_error(HTTPStatus.BAD_REQUEST, "INVALID_REQUEST")
                return
            relative = "index.html" if parsed.path == "/" else parsed.path[1:]
            path = _safe_static_path(static_root, relative)
            if path is None:
                self._send_error(HTTPStatus.NOT_FOUND, "INVALID_REQUEST")
                return
            try:
                content = path.read_bytes()
            except (OSError, ValueError):
                self._send_error(HTTPStatus.NOT_FOUND, "INVALID_REQUEST")
                return
            self._send_bytes(HTTPStatus.OK, content, _SUPPORTED_TYPES[path.suffix.lower()])

        def _send_error(self, status: HTTPStatus, code: str) -> None:
            self._send_json(status, {"error": {"code": code}})

        def _send_json(self, status: HTTPStatus, payload: dict[str, object]) -> None:
            body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            self._send_bytes(status, body, "application/json; charset=utf-8")

        def _send_bytes(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", _CSP)
            self.end_headers()
            if getattr(self, "command", None) != "HEAD":
                self.wfile.write(body)

    return LocalHandler


def _single_param(params: dict[str, list[str]], name: str) -> str | None:
    values = params.get(name)
    return None if values is None else values[0]


def _safe_static_path(static_root: Path, relative: str) -> Path | None:
    """Resolve one prototype file while rejecting traversal and symlinks."""
    try:
        decoded = unquote(relative)
    except (UnicodeError, ValueError):
        return None
    if not decoded or "\x00" in decoded or "\\" in decoded:
        return None
    parts = decoded.split("/")
    if any(not part or part in {".", ".."} or part.startswith(".") for part in parts):
        return None
    if Path(parts[-1]).suffix.lower() not in _SUPPORTED_TYPES:
        return None
    candidate = static_root.joinpath(*parts)
    try:
        root_stat = os.lstat(static_root)
        if not stat.S_ISDIR(root_stat.st_mode):
            return None
        current = static_root
        for part in parts:
            current = current / part
            item_stat = os.lstat(current)
            if stat.S_ISLNK(item_stat.st_mode):
                return None
        candidate_stat = os.lstat(candidate)
        if not stat.S_ISREG(candidate_stat.st_mode):
            return None
        return candidate
    except OSError:
        return None


def _default_work_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    """Run the local bridge until interrupted."""
    parser = argparse.ArgumentParser(description="Run the local NegritaOS 360 bridge")
    parser.add_argument("--port", type=int, default=8791)
    parser.add_argument("--access-file", type=Path)
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    work_root = _default_work_root()
    access_path = args.access_file or work_root / ".local" / "dashboard-access.json"
    server = create_local_server(work_root, access_path, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
