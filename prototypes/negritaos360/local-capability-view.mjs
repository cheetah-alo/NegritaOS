import {esc, heading} from './components.mjs';
import {selectLocalCapabilities} from './local-capabilities.mjs';

const LABELS = {agent: 'Agentes', skill: 'Skills', rule: 'Reglas'};
const CONFIGURATION_COPY = {
  REGISTERED: 'Registrada',
  RESOLVED: 'Resuelta',
  DECLARED: 'Declarada',
};

function stateView(title, message, retry = false) {
  return heading('CAPACIDADES LOCALES', title, message) +
    `<section class="panel local-capability-state"><span aria-hidden="true">${retry ? '!' : '◎'}</span>` +
    `<p>${esc(message)}</p>${retry ? '<button class="button primary" data-local-capabilities-retry>Reintentar lectura</button>' : ''}</section>`;
}

function kindCounts(items) {
  return Object.keys(LABELS).map(kind =>
    `<article class="metric local-capability-count"><span>${LABELS[kind].toUpperCase()}</span>` +
    `<strong>${items.filter(item => item.kind === kind).length}</strong><small>Relaciones con proyectos</small></article>`).join('');
}

function capabilityCards(items) {
  return Object.keys(LABELS).map(kind => {
    const group = items.filter(item => item.kind === kind);
    if (!group.length) return '';
    return `<section class="local-capability-group" data-capability-kind="${kind}">` +
      `<div class="panel-heading"><h2>${LABELS[kind]}</h2><span class="muted">${group.length} relaciones</span></div>` +
      `<div class="table-wrap"><table><thead><tr><th>Nombre</th><th>Proyecto</th><th>Configuración</th></tr></thead><tbody>` +
      group.map(item => {
        const reference = item.id === item.name ? '' :
          `<small title="${esc(item.id)}">Ref. ${esc(item.id.slice(0, 17))}…</small>`;
        return `<tr><td><span class="local-capability-name">${esc(item.name)}</span>${reference}</td>` +
        `<td><button class="project-link" data-project="${esc(item.project_id)}">${esc(item.project_id)}</button></td>` +
        `<td><span class="type-label">${CONFIGURATION_COPY[item.configuration_state]}</span></td></tr>`;
      }).join('') +
      `</tbody></table></div></section>`;
  }).join('');
}

export function renderLocalCapabilityView(catalog, filters = {}) {
  if (!catalog || catalog.status === 'loading' || catalog.status === 'idle') {
    return stateView('Leyendo capacidades locales…', 'La lectura ocurre sólo en este equipo.');
  }
  if (catalog.status === 'error') {
    return stateView('No se pudieron leer las capacidades locales.', 'Comprueba el servidor y la política local de acceso.', true);
  }
  if (catalog.status === 'EMPTY' || catalog.state === 'EMPTY') {
    return stateView('No hay capacidades visibles.', 'La política local aún no concede agentes, skills o reglas a esta vista.');
  }

  const sourceItems = catalog.items || [];
  const items = selectLocalCapabilities(sourceItems, filters);
  const selectedKind = ['agent', 'skill', 'rule'].includes(filters.kind) ? filters.kind : 'all';
  const selector = `<label class="local-capability-kind-filter">Tipo` +
    `<select data-kind-selector><option value="all"${selectedKind === 'all' ? ' selected' : ''}>Todos</option>` +
    Object.entries(LABELS).map(([kind, label]) => `<option value="${kind}"${selectedKind === kind ? ' selected' : ''}>${label}</option>`).join('') +
    `</select></label>`;
  const content = items.length ? capabilityCards(items) :
    `<div class="local-no-match"><p>Ninguna capacidad coincide con estos filtros.</p>` +
    `<button class="button text" data-local-capabilities-clear>Limpiar filtros</button></div>`;
  return heading('FUENTE LOCAL · CAPACIDADES', 'Capacidades configuradas en esta vista.',
    'Cada fila vincula una capacidad a un proyecto permitido; una misma capacidad puede aparecer varias veces. No acredita uso ni ejecución.') +
    `<div class="local-capability-summary">${kindCounts(items)}</div>` +
    `<div class="local-capability-toolbar">${selector}</div>` +
    `<div class="local-capability-groups">${content}</div>` +
    `<div class="contract-note"><b>Lectura local en modo informativo.</b> ` +
    `Configuración local declarada; no indica uso ni evidencia. ` +
    `Los estados describen configuración declarada por la fuente; no equivalen a actividad observada o validación de contenido.</div>`;
}
