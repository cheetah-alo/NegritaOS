import test from 'node:test';
import assert from 'node:assert/strict';
import {fetchLocalCapabilities, parseLocalCapabilities, selectLocalCapabilities} from './local-capabilities.mjs';
import {renderLocalCapabilityView,renderLocalAgentView} from './local-capability-view.mjs';

const digest = 'a'.repeat(64);
const item = {id: 'agent_one', project_id: 'alpha', kind: 'agent', name: 'Agent One', description: 'Reviews code.', configuration_state: 'REGISTERED'};
const response = items => ({state: items.length ? 'READY' : 'EMPTY', items, provenance: {snapshot_id: 'view-local', view_sha256: digest}});

test('parses the strict allowlisted capabilities contract', () => {
  assert.equal(parseLocalCapabilities(response([item])).items[0].name, 'Agent One');
  assert.throws(() => parseLocalCapabilities(response([{...item, extra: true}])), /inválido/);
  assert.throws(() => parseLocalCapabilities(response([{...item, description: []}])), /inválido/);
  assert.throws(() => parseLocalCapabilities(response([{...item, configuration_state: 'USED'}])), /inválido/);
  assert.throws(() => parseLocalCapabilities({...response([]), state: 'READY'}), /inconsistente/);
  assert.equal(parseLocalCapabilities(response([
    item, {...item, project_id: 'beta'},
  ])).items.length, 2);
  assert.equal(parseLocalCapabilities(response([{...item, description: null}])).items[0].description, null);
});

test('fetches same-origin capabilities with optional filters and no-store', async () => {
  let called;
  const result = await fetchLocalCapabilities(async (url, options) => {
    called = {url, options};
    return {ok: true, json: async () => response([item])};
  }, {project: 'alpha', kind: 'agent'});
  assert.equal(called.url, '/api/v1/capabilities?project_id=alpha&kind=agent');
  assert.equal(called.options.cache, 'no-store');
  assert.equal(called.options.credentials, 'same-origin');
  assert.equal(result.items[0].id, 'agent_one');
  await assert.rejects(() => fetchLocalCapabilities(async () => ({ok: false})), /no disponibles/);
});

test('filters already authorized items without inventing capabilities', () => {
  const items = [item, {...item, id: 'skill_one', kind: 'skill', name: 'Search skill', description: null, project_id: 'beta'}];
  assert.deepEqual(selectLocalCapabilities(items, {kind: 'skill'}).map(entry => entry.id), ['skill_one']);
  assert.deepEqual(selectLocalCapabilities(items, {project: 'gamma'}), []);
  assert.deepEqual(selectLocalCapabilities(items, {search: 'SEARCH'}).map(entry => entry.id), ['skill_one']);
  assert.deepEqual(selectLocalCapabilities(items, {search: 'reviews code'}).map(entry => entry.id), ['agent_one']);
});

test('renders escaped names, configuration wording, and explicit non-usage boundary', () => {
  const html = renderLocalCapabilityView(parseLocalCapabilities(response([{...item, name: '<script>Injected</script>'}])), {});
  assert.match(html, /&lt;script&gt;Injected&lt;\/script&gt;/);
  assert.match(html, /Configuración local declarada; no indica uso ni evidencia/);
  assert.doesNotMatch(html, /Atlas|USED|observaciones|8 resultados/);
  assert.doesNotMatch(html, /<script>/);
  assert.match(html, /<button[^>]+data-project="alpha"/);
  assert.match(html, /Reviews code\./);
});

test('agent view groups project relationships and escapes canonical descriptions', () => {
  const catalog = parseLocalCapabilities(response([
    {...item, name: 'Gisel · Project Hours Tracker', description: '<script>bad</script>'},
    {...item, name: 'Gisel · Project Hours Tracker', description: '<script>bad</script>', project_id: 'beta'},
  ]));
  const html = renderLocalAgentView(catalog);
  assert.match(html, /1 agentes distintos · 2 relaciones/);
  assert.match(html, /&lt;script&gt;bad&lt;\/script&gt;/);
  assert.doesNotMatch(html, /<script>/);
  assert.match(html, /data-project="alpha"/);
  assert.match(html, /data-project="beta"/);
  assert.match(renderLocalAgentView(catalog, {project: 'beta'}), /1 relaciones/);
});

test('keeps loading, empty, error, and retry states distinct', () => {
  assert.match(renderLocalCapabilityView({status: 'loading'}), /Leyendo capacidades locales/);
  assert.match(renderLocalCapabilityView({status: 'EMPTY'}), /No hay capacidades visibles/);
  assert.match(renderLocalCapabilityView({status: 'error'}), /Reintentar lectura/);
});
