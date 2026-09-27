import { clients, projects } from './data.mjs';
import { state, selectProjects } from './state.mjs';
import { esc, heading, empty } from './components.mjs';
import { createTracks, progress, featureState, activationProblems } from './tracking-model.mjs';

export const tracking = { tracks: createTracks(), tab: 'plan', versions: {}, message: '' };
export function resetTracking() {
  Object.assign(tracking, { tracks: createTracks(), tab: 'plan', versions: {}, message: '' });
}
export function currentTrack() {
  const allowed = selectProjects({ ...state, search: '' });
  const project = allowed[0];
  if (!project) return null;
  const track = tracking.tracks[project.id];
  const spec = track.revisions.find(r => r.id === tracking.versions[project.id]) ||
    track.revisions.find(r => r.id === track.activeId) || track.revisions[0];
  return { project, track, spec };
}
const clientName = project => clients.find(c => c.id === project.clientId)?.name || 'Sin cliente';
const tag = (value, tone = '') => `<span class="track-tag ${tone}">${esc(value)}</span>`;

function planContent(project, track, spec) {
  const p = progress(track, spec);
  return `<div class="plan-grid"><section class="panel goal-panel">
    <p class="eyebrow">01 / OBJETIVO · ${esc(spec.goal.id)}</p><h2>${esc(spec.goal.statement)}</h2>
    <p class="goal-context">Cada funcionalidad debe aportar a este objetivo. El avance de entrega no demuestra su consecución.</p>
    <div class="goal-target"><div><span>RESULTADO ESPERADO</span><strong>${spec.goal.direction} ${spec.goal.target} <small>${esc(spec.goal.unit)}</small></strong></div><p>${esc(spec.goal.metric)}<small>${esc(spec.goal.window)}</small></p></div>
    <div class="goal-baseline"><span>Línea base <b>Sin medir</b></span><span>Resultado observado <b>Sin medir</b></span></div>
    <div class="spec-columns"><div><h3>Dentro del alcance</h3><p>${esc(spec.scope)}</p></div><div><h3>Fuera del alcance</h3><p>${esc(spec.exclusions)}</p></div></div>
    <div class="design-reference"><span>▧</span><div><b>Diseño funcional versionado</b><small>${esc(spec.designRef || 'Pendiente de definición')} · estructura, interacción y criterios</small></div></div></section>
    <aside class="panel progress-panel"><p class="eyebrow">02 / ENTREGA VALIDADA</p>
    <div class="progress-number">${track.activeId === spec.id ? p.percent + '<small>%</small>' : '—'}</div>
    <progress max="100" value="${track.activeId === spec.id ? p.percent : 0}" aria-label="Avance validado del plan"></progress>
    <p><b>${p.done} de ${p.total}</b> funcionalidades con evidencia sintética compatible.</p>
    <div class="progress-facts"><div><span>Versión consultada</span><b>v${spec.version}</b></div><div><span>Estado</span><b>${track.activeId === spec.id ? 'Activa · demo' : 'No activa'}</b></div><div><span>Medición del objetivo</span><b>Desconocida</b></div></div>
    <p class="annotation">Peso igual por funcionalidad. Un commit o una tarea en curso no aumenta este porcentaje.</p>
    <button class="button secondary" data-track-tab="features">Ver funcionalidades →</button></aside></div>`;
}

function featureContent(track, spec) {
  const query = state.search.trim().toLowerCase();
  const items = spec.features.filter(f => `${f.id} ${f.name} ${f.criterion}`.toLowerCase().includes(query));
  return `<section class="panel"><div class="panel-heading"><h2>Alcance verificable</h2><span class="muted">${items.length} funcionalidades · v${spec.version}</span></div>
    ${items.length ? `<div class="table-wrap"><table class="feature-table"><thead><tr><th>ID / funcionalidad</th><th>Criterio de aceptación</th><th>Responsable</th><th>Estado</th><th>Detalle</th></tr></thead><tbody>${items.map(f => `<tr><td><small>${f.id}</small><b>${esc(f.name)}</b></td><td class="criterion-cell">${esc(f.criterion)}</td><td>${esc(f.owner)}</td><td>${tag(featureState(track, spec, f), featureState(track, spec, f) === 'Validada' ? 'success' : '')}</td><td><button class="button text" data-track-task="${f.id}" aria-label="Ver ${f.id}">Ver →</button></td></tr>`).join('')}</tbody></table></div>` : empty('No hay funcionalidades con ese término. Prueba otra búsqueda.')}</section>
    <div class="contract-note"><b>Definición → implementación → comprobación → aceptación.</b><span>La evidencia debe corresponder al criterio y diseño vigentes. Las dependencias bloquean la validación; los commits son referencias, no aprobaciones.</span></div>`;
}

function versionContent(track, spec) {
  const base = track.revisions.find(r => r.id === spec.parentId);
  const candidate = !track.activations.some(a => a.revisionId === spec.id);
  return `<div class="plan-grid"><section class="panel revision-panel"><p class="eyebrow">CONTROL DE CAMBIOS</p><h2>${base ? `v${base.version} → v${spec.version}` : 'Una línea base, explícita.'}</h2><p>${esc(spec.change.reason)}</p>
    <div class="version-comparison"><div><span>${base ? 'VERSIÓN ANTERIOR' : 'ANTES DE ACTIVAR'}</span><strong>${base ? base.features.length : '—'}<small> funcionalidades</small></strong><p>${base ? 'Se conserva el alcance anterior.' : 'No existe avance de una línea base activa.'}</p></div><div><span>VERSIÓN CONSULTADA</span><strong>${spec.features.length}<small> funcionalidades</small></strong><p>${candidate ? 'Candidata; todavía no cambia el plan activo.' : 'Registro conservado en el historial.'}</p></div></div>
    <div class="change-detail">${spec.change.kind === 'add' ? '+ Nueva funcionalidad. La evidencia compatible se conserva; cambia el denominador.' : spec.change.kind === 'criterion' ? '↻ Cambia el criterio F-02. Su evidencia anterior no valida la nueva definición.' : 'Goal, alcance, diseño, owners y criterios se fijan al activar.'}</div>
    <p class="annotation">Resultado objetivo: sin medir. No se reconstruye el avance pasado con el alcance nuevo.</p></section>
    <section class="panel history-panel"><p class="eyebrow">HISTORIAL DE ACTIVACIÓN</p>${track.activations.map(a => `<article><span class="history-point"></span><div><b>v${track.revisions.find(r => r.id === a.revisionId).version} activada</b><p>${a.percent}% al activar · ${esc(a.actor)}</p><small>Evento demo ${a.sequence} · preservado</small></div></article>`).join('') || '<p>Ninguna versión activada aún.</p>'}</section></div>`;
}

export function trackingView() {
  const current = currentTrack();
  if (!current) return heading('SEGUIMIENTO POR PROYECTO', 'Del plan al resultado.', 'Selecciona un proyecto autorizado.') + empty();
  const { project, track, spec } = current;
  const candidates = track.revisions.filter(r => !track.activations.some(a => a.revisionId === r.id));
  const problems = activationProblems(track, spec);
  const active = track.activeId === spec.id;
  const historical = track.activations.some(a => a.revisionId === spec.id) && !active;
  return heading('PROYECTOS / PLANES Y AVANCE', 'Un objetivo. Un plan. Cada cambio, visible.', 'Define lo que quieres conseguir, activa una versión y mide sólo lo que puedas demostrar.') +
    `<div class="track-projects">${selectProjects({ ...state, project: 'all', search: '' }).map(p => `<button data-track-project="${p.id}" aria-pressed="${project.id === p.id}"><span>${esc(clientName(p))}</span><b>${esc(p.name)}</b><small>${tracking.tracks[p.id].activeId ? 'Plan activo · demo' : 'Por activar'}</small></button>`).join('')}</div>
    <div class="plan-identity"><div><p>${esc(clientName(project))} <span>/</span> ${esc(project.name)} <span>/</span> PLAN-${project.id.toUpperCase()}</p><h2>${esc(spec.title)}</h2><span class="plan-owner">${esc(spec.owner)} · Diseño ${esc(spec.designRef || 'pendiente')}</span></div><div class="plan-actions">${tag(active ? 'Activa · demo' : historical ? 'Histórica' : 'Candidata', active ? 'success' : '')}<label class="sr-only" for="plan-version">Versión del plan</label><select id="plan-version">${track.revisions.map(r => `<option value="${r.id}" ${r.id === spec.id ? 'selected' : ''}>v${r.version}${r.id === track.activeId ? ' · activa' : ''}</option>`).join('')}</select>
    ${active ? `<button class="button primary" data-propose ${candidates.length ? 'disabled' : ''}>Proponer cambio +</button>` : !historical ? `<button class="button primary" data-activate ${problems.length ? 'disabled' : ''}>Revisar activación →</button>` : ''}</div></div>
    ${candidates.length && active ? `<div class="candidate-notice">Hay una revisión candidata. La versión activa no ha cambiado. <button class="text-button" data-select-candidate="${candidates[0].id}">Ver candidata →</button></div>` : ''}
    ${problems.length ? `<div class="stale-banner"><b>No se puede activar:</b> ${problems.map(esc).join(' · ')}</div>` : ''}
    ${tracking.message ? `<p class="track-feedback" role="status">${esc(tracking.message)}</p>` : ''}
    <div class="track-tabs">${[['plan', 'Plan y objetivo'], ['features', 'Funcionalidades'], ['versions', 'Versiones y cambios']].map(([id, label]) => `<button data-track-tab="${id}" aria-pressed="${tracking.tab === id}">${label}</button>`).join('')}<span>SIMULACIÓN VOLÁTIL · SE REINICIA AL RECARGAR</span></div>
    ${{ plan: () => planContent(project, track, spec), features: () => featureContent(track, spec), versions: () => versionContent(track, spec) }[tracking.tab]()}`;
}
