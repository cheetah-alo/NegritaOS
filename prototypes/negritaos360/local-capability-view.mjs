import {esc, heading} from './components.mjs';
import {selectLocalCapabilities} from './local-capabilities.mjs';

const LABELS = {agent: 'Agentes', skill: 'Skills', rule: 'Reglas'};
const CONFIGURATION_COPY = {
  REGISTERED: 'Registrada',
  RESOLVED: 'Resuelta',
  DECLARED: 'Declarada',
  MIXED: 'Mixta',
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
      `<div class="table-wrap"><table><thead><tr><th>Nombre y función</th><th>Proyecto</th><th>Configuración</th></tr></thead><tbody>` +
      group.map(item => {
        const reference = item.id === item.name ? '' : item.kind === 'agent' ?
          `<small class="local-agent-id">ID: ${esc(item.id)}</small>` :
          `<small title="${esc(item.id)}">Ref. ${esc(item.id.slice(0, 17))}…</small>`;
        const description = item.kind === 'agent' ?
          `<span class="local-agent-description">${esc(item.description || 'Descripción no registrada en integrator.yaml.')}</span>` : '';
        return `<tr><td><span class="local-capability-name">${esc(item.name)}</span>${description}${reference}</td>` +
        `<td><button class="project-link" data-project="${esc(item.project_id)}">${esc(item.project_id)}</button></td>` +
        `<td><span class="type-label">${CONFIGURATION_COPY[item.configuration_state]}</span></td></tr>`;
      }).join('') +
      `</tbody></table></div></section>`;
  }).join('');
}

export function renderLocalAgentView(catalog, filters = {}) {
  if (!catalog || ['loading', 'idle'].includes(catalog.status)) {
    return stateView('Leyendo agentes locales…', 'La lectura ocurre sólo en este equipo.');
  }
  if (catalog.status === 'error') {
    return stateView('No se pudieron leer los agentes locales.', 'Comprueba el servidor y la política local de acceso.', true);
  }
  if (catalog.status === 'EMPTY' || catalog.state === 'EMPTY') {
    return stateView('No hay agentes visibles.', 'La política local no permite mostrar agentes de proyectos en esta vista.');
  }
  const rows = selectLocalCapabilities(catalog.items || [], {...filters, kind: 'agent'});
  const agents = new Map();
  for (const row of rows) {
    if (!agents.has(row.id)) agents.set(row.id, {...row, projects: []});
    if (agents.get(row.id).configuration_state !== row.configuration_state) {
      agents.get(row.id).configuration_state = 'MIXED';
    }
    agents.get(row.id).projects.push(row.project_id);
  }
  const cards = [...agents.values()].sort((a, b) => a.name.localeCompare(b.name, 'es'));
  const content = cards.length ? cards.map(agent =>
    `<article class="panel local-agent-card"><div class="panel-heading"><h2>${esc(agent.name)}</h2>` +
    `<span class="type-label">${CONFIGURATION_COPY[agent.configuration_state]}</span></div>` +
    `<p class="local-agent-description">${esc(agent.description || 'Descripción no registrada en integrator.yaml.')}</p>` +
    `<small class="local-agent-id">ID: ${esc(agent.id)}</small>` +
    `<div class="local-agent-projects"><span>Proyectos vinculados · ${agent.projects.length}</span>` +
    agent.projects.map(project => `<button class="project-link" data-project="${esc(project)}">${esc(project)}</button>`).join('') +
    `</div></article>`).join('') :
    `<div class="local-no-match"><p>Ningún agente coincide con estos filtros.</p>` +
    `<button class="button text" data-local-capabilities-clear>Limpiar filtros</button></div>`;
  return heading('FUENTE LOCAL · AGENTES', 'Quién hace qué en NegritaOS.',
    'Nombres y funciones del registro canónico, vinculados sólo a los proyectos permitidos en este equipo.') +
    `<div class="local-agent-summary">${cards.length} agentes distintos · ${rows.length} relaciones con proyectos</div>` +
    `<div class="local-agent-grid">${content}</div>` +
    `<div class="contract-note"><b>Configuración, no actividad.</b> ` +
    `La descripción procede de integrator.yaml. La asociación con un proyecto no demuestra uso, ejecución o validación.</div>`;
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
