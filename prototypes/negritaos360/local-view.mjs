import {esc, heading} from './components.mjs';
import {selectLocalProjects} from './local-catalog.mjs';

function localStatus(title, message, retry = false) {
  const action = retry ? '<button class="button primary" data-local-retry>Reintentar lectura</button>' : '';
  return heading('CATÁLOGO LOCAL', title, message) +
    `<section class="panel local-state">
      <span aria-hidden="true">${retry ? '!' : '◎'}</span>
      <p>${esc(message)}</p>${action}
    </section>`;
}

function clientLabel(project) {
  if (project.client_classification === 'unknown') return 'Sin clasificar';
  if (project.client_classification === 'internal') return 'Interno';
  return project.client_id;
}

function projectRows(items) {
  return items.map(project => `<tr>
    <td><button class="name-link" data-project="${esc(project.project_id)}">
      ${esc(project.name)} <span>↗</span></button><small>${esc(project.project_id)}</small></td>
    <td>${esc(clientLabel(project))}</td>
    <td><span class="type-label">${esc(project.client_classification)}</span></td>
  </tr>`).join('');
}

export function renderLocalView(route, catalog, filters = {}) {
  if (catalog.status === 'loading' || catalog.status === 'idle') {
    return localStatus('Leyendo el catálogo autorizado…', 'La lectura ocurre sólo en este equipo.');
  }
  if (catalog.status === 'error') {
    return localStatus('No se pudo leer el catálogo local.', 'Comprueba el servidor y la política local de acceso.', true);
  }
  if (catalog.status === 'EMPTY') {
    return localStatus('No hay proyectos visibles.', 'La política local aún no concede proyectos a esta vista.');
  }
  if (!['overview', 'projects'].includes(route)) {
    return heading('FUENTE LOCAL · EN PREPARACIÓN', 'Esta sección todavía no está conectada.',
      'El catálogo de proyectos ya se lee en local. Las otras secciones esperan sus contratos y fuentes.') +
      `<section class="panel local-state">
        <p>Para explorar el flujo visual completo, cambia la fuente a Demo.</p>
        <button class="button secondary" data-switch-demo>Ver demo →</button>
      </section>`;
  }
  const projects = selectLocalProjects(catalog.projects, filters);
  const title = route === 'projects' ? 'Proyectos de esta vista.' : 'Tu catálogo local, a la vista.';
  const subtitle = 'Sólo aparecen proyectos incluidos en la política local de acceso.';
  const table = projects.length ? `<div class="table-wrap"><table>
    <thead><tr><th>Proyecto</th><th>Cliente</th><th>Clasificación</th></tr></thead>
    <tbody>${projectRows(projects)}</tbody></table></div>` :
    `<div class="local-no-match">Ningún proyecto coincide con estos filtros.
      <button class="button text" data-local-clear>Limpiar filtros</button></div>`;
  return heading('FUENTE LOCAL · PROYECTOS', title, subtitle,
    '<button class="button primary" data-route="catalog">Ver capacidades →</button>') +
    `<div class="local-summary">
      <article class="metric"><span>PROYECTOS EN ESTA VISTA</span><strong>${projects.length}</strong>
        <small>Filtro aplicado al ámbito autorizado</small></article>
      <article class="metric local-context"><span>GOAL Y UTILIZACIÓN</span><strong>Sin medir</strong>
        <small>La fuente local aún no incluye goals, skills ni uso.</small></article>
    </div>` +
    `<section class="panel"><div class="panel-heading"><h2>Proyectos</h2>
      <span class="muted">Lectura local · ${esc(catalog.provenance.snapshot_id)}</span>
    </div>${table}</section>` +
    `<div class="contract-note"><b>Catálogo local en lectura.</b>
      <span>La lista no acredita actividad de Brain, progreso del plan ni utilización de capacidades.</span>
    </div>`;
}
