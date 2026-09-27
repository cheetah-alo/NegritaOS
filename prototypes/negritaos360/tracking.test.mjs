import test from 'node:test';
import assert from 'node:assert/strict';
import { createTracks, progress, activationProblems, proposeRevision, activateRevision,
  validateFeature, featureState } from './tracking-model.mjs';
import { selectProjects, selectCapabilities, state } from './state.mjs';
import { projects, clients, navItems } from './data.mjs';
import { renderView } from './views.mjs';

test('fixtures bind every project to an explicit demo client', () => {
  assert.ok(projects.every(p => clients.some(c => c.id === p.clientId)));
  const scope = { project: 'all', client: 'client-b', search: '', kind: 'Todos' };
  assert.deepEqual(selectProjects(scope).map(p => p.id), ['faro']);
  assert.ok(selectCapabilities(scope).every(c => c.project === 'faro'));
  assert.equal(selectProjects({ ...scope, project: 'atlas' }).length, 0);
});
test('accepted progress is separate from unknown goal achievement', () => {
  const track = createTracks().atlas;
  assert.equal(progress(track, track.revisions[0]).percent, 40);
  assert.equal(track.revisions[0].goal.actual, null);
});
test('adding scope does not mutate or activate the original definition', () => {
  const track = createTracks().atlas;
  const original = JSON.stringify(track.revisions[0]);
  const revision = proposeRevision(track, 'add', 'Comparar versiones');
  assert.equal(JSON.stringify(track.revisions[0]), original);
  assert.equal(track.activeId, 'atlas-v1');
  assert.equal(revision.features.length, 6);
  assert.equal(progress(track, revision).percent, 33);
  assert.throws(() => { revision.goal.target = 100; }, TypeError);
});
test('candidate requires reason and only one open candidate is allowed', () => {
  const track = createTracks().atlas;
  assert.throws(() => proposeRevision(track, 'add', ' '));
  assert.throws(() => proposeRevision(track, 'untyped', 'Motivo'));
  proposeRevision(track, 'add', 'Motivo');
  assert.throws(() => proposeRevision(track, 'criterion', 'Otro motivo'));
});
test('criterion change requires new evidence for the affected functionality', () => {
  const track = createTracks().atlas;
  const candidate = proposeRevision(track, 'criterion', 'Aislamiento por cliente');
  assert.equal(progress(track, candidate).percent, 20);
  assert.equal(progress(track, track.revisions[0]).percent, 40);
});
test('activation needs confirmation and preserves the old history point', () => {
  const track = createTracks().atlas;
  const candidate = proposeRevision(track, 'add', 'Scope nuevo');
  assert.throws(() => activateRevision(track, candidate.id, false));
  activateRevision(track, candidate.id, true);
  assert.equal(track.activeId, candidate.id);
  assert.deepEqual(track.activations.map(a => a.percent), [40, 33]);
  assert.throws(() => activateRevision(track, candidate.id, true));
  assert.throws(() => activateRevision(track, 'atlas-v1', true));
});
test('a project without versioned design cannot activate', () => {
  const track = createTracks().faro;
  assert.ok(activationProblems(track, track.revisions[0]).includes('Falta diseño versionado'));
  assert.throws(() => activateRevision(track, track.revisions[0].id, true));
});
test('draft project becomes active only after explicit confirmation', () => {
  const track = createTracks().brisa;
  assert.equal(track.activeId, null);
  activateRevision(track, 'brisa-v1', true);
  assert.equal(track.activeId, 'brisa-v1');
  assert.equal(progress(track, track.revisions[0]).percent, 0);
});
test('missing and cyclic dependencies are rejected before activation', () => {
  const track = createTracks().brisa;
  const candidate = structuredClone(track.revisions[0]);
  candidate.features[0].dependencies = ['F-03'];
  assert.ok(activationProblems(track, candidate).includes('Dependencias cíclicas'));
  candidate.features[0].dependencies = ['missing'];
  assert.ok(activationProblems(track, candidate).includes('Dependencia inexistente'));
});
test('blocked work and historical versions cannot receive accepted demo evidence', () => {
  const track = createTracks().atlas;
  const spec = track.revisions[0];
  assert.equal(featureState(track, spec, spec.features[3]), 'Bloqueada');
  assert.throws(() => validateFeature(track, spec.id, 'F-04'));
  validateFeature(track, spec.id, 'F-03');
  assert.equal(progress(track, spec).percent, 60);
  assert.throws(() => validateFeature(track, spec.id, 'F-03'));
  const next = proposeRevision(track, 'add', 'Nueva funcionalidad');
  activateRevision(track, next.id, true);
  assert.throws(() => validateFeature(track, spec.id, 'F-05'));
});
test('foreign project evidence cannot increase progress; empty scope is not zero percent', () => {
  const track = createTracks().brisa;
  track.receipts.push({ project: 'atlas', acceptanceKey: 'brisa:F-01:1', status: 'accepted' });
  assert.equal(progress(track, track.revisions[0]).done, 0);
  assert.equal(progress(track, { features: [] }).percent, null);
});
test('all eight routes render in all five read states', () => {
  const old = { ...state };
  try {
    for (const [route] of navItems) for (const scenario of ['ready', 'loading', 'empty', 'error', 'stale']) {
      Object.assign(state, { route, scenario, client: 'all', project: 'all', search: '' });
      assert.match(renderView(), /<h1>/);
    }
  } finally { Object.assign(state, old); }
});
test('demo agents route shows only synthetic agent roles', () => {
  const old = { ...state };
  try {
    Object.assign(state, { route: 'agents', scenario: 'ready', client: 'all', project: 'all', search: '' });
    const html = renderView();
    assert.match(html, /AGENTES · DEMO/);
    assert.match(html, /Arquitectura de software/);
    assert.doesNotMatch(html, /pablo_deployment_operator_agent/);
  } finally { Object.assign(state, old); }
});
