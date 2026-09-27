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

export function renderLocalAgentView(catalog, filters = {}, projectNames = {}) {
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
  const directory = [...agents.values()].sort((a, b) => a.name.localeCompare(b.name, 'es'));
  const missing = directory.filter(agent => !agent.description).length;
  const content = directory.length ? directory.map((agent, index) => {
    const description = agent.description || 'Descripción no registrada en integrator.yaml.';
    const projectCount = agent.projects.length;
    return `<details class="local-agent-entry" name="local-agent-directory"><summary>` +
      `<span class="local-agent-number" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span>` +
      `<span class="local-agent-primary"><strong>${esc(agent.name)}</strong>` +
      `<small aria-hidden="true">${esc(description)}</small></span>` +
      `<span class="local-agent-count">${projectCount} ${projectCount === 1 ? 'proyecto' : 'proyectos'}</span>` +
      `<span class="local-agent-chevron" aria-hidden="true">⌄</span></summary>` +
      `<div class="local-agent-detail"><div class="local-agent-function">` +
      `<span class="local-agent-detail-label">FUNCIÓN DECLARADA</span>` +
      `<p>${esc(description)}</p><span class="type-label">${CONFIGURATION_COPY[agent.configuration_state]}</span>` +
      `<small class="local-agent-id">ID: ${esc(agent.id)}</small></div>` +
      `<div class="local-agent-affiliations"><span class="local-agent-detail-label">PROYECTOS VINCULADOS · ${projectCount}</span>` +
      `<div class="local-agent-projects">` + agent.projects.map(project =>
        `<button class="project-link" data-project="${esc(project)}" title="Abrir proyecto ${esc(projectNames[project] || project)}">${esc(projectNames[project] || project)}<span aria-hidden="true">↗</span></button>`
      ).join('') + `</div></div></div></details>`;
  }).join('') :
    `<div class="local-no-match"><p>Ningún agente coincide con estos filtros.</p>` +
    `<button class="button text" data-local-capabilities-clear>Limpiar filtros</button></div>`;
  return heading('FUENTE LOCAL · AGENTES', 'Agentes de tu ecosistema.',
    'Recorre sus funciones y abre sólo el contexto de proyecto que necesites.') +
    `<div class="local-agent-summary"><span><strong>${directory.length}</strong> agentes distintos</span>` +
    `<span><strong>${rows.length}</strong> relaciones con proyectos</span>` +
    `<span class="${missing ? 'local-agent-summary-attention' : ''}"><strong>${missing}</strong> sin descripción</span></div>` +
    `<section class="local-agent-directory" aria-label="Directorio de agentes">${content}</section>` +
    `<div class="contract-note"><b>Configuración, no actividad.</b> ` +
    `La descripción original procede de integrator.yaml. La asociación con un proyecto no demuestra uso, ejecución o validación.</div>`;
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
