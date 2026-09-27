// Same-origin read model only. This module never reads registries or local files.
const ID = /^[a-z][a-z0-9_-]*$/;
const HASH = /^[0-9a-f]{64}$/;
const PROJECT_KEYS = ['project_id', 'name', 'client_id', 'client_classification'];

export function parseLocalCatalog(payload) {
  if (!payload || typeof payload !== 'object' || !['READY', 'EMPTY'].includes(payload.state) ||
      !Array.isArray(payload.projects) || !payload.provenance || typeof payload.provenance !== 'object') {
    throw new Error('Contrato de catálogo local inválido');
  }
  const {snapshot_id: snapshotId, view_sha256: viewSha256} = payload.provenance;
  if (typeof snapshotId !== 'string' || !/^view-[0-9a-f]{20}$/.test(snapshotId) ||
      typeof viewSha256 !== 'string' || !HASH.test(viewSha256)) {
    throw new Error('Procedencia del catálogo local inválida');
  }
  const seen = new Set();
  const projects = payload.projects.map(project => {
    if (!project || typeof project !== 'object' ||
        Object.keys(project).sort().join(',') !== [...PROJECT_KEYS].sort().join(',') ||
        typeof project.project_id !== 'string' || !ID.test(project.project_id) ||
        typeof project.name !== 'string' || !project.name.trim() || seen.has(project.project_id)) {
      throw new Error('Proyecto del catálogo local inválido');
    }
    const {client_id: clientId, client_classification: kind} = project;
    const consistent = kind === 'unknown' ? clientId === null :
      kind === 'internal' ? clientId === 'internal' :
      kind === 'known' && typeof clientId === 'string' && ID.test(clientId) && clientId !== 'internal';
    if (!consistent) throw new Error('Cliente del catálogo local inválido');
    seen.add(project.project_id);
    return {project_id: project.project_id, name: project.name.trim(), client_id: clientId,
      client_classification: kind};
  });
  if ((payload.state === 'EMPTY') !== (projects.length === 0)) {
    throw new Error('Estado del catálogo local inconsistente');
  }
  return {state: payload.state, projects, provenance: {snapshot_id: snapshotId, view_sha256: viewSha256}};
}

export async function fetchLocalCatalog(fetcher = fetch) {
  const response = await fetcher('/api/v1/catalog', {
    method: 'GET', cache: 'no-store', credentials: 'same-origin', headers: {Accept: 'application/json'},
  });
  if (!response.ok) throw new Error('Catálogo local no disponible');
  return parseLocalCatalog(await response.json());
}

export function selectLocalProjects(projects, {client = 'all', project = 'all', search = ''} = {}) {
  const query = search.trim().toLocaleLowerCase('es');
  return projects.filter(item =>
    (client === 'all' || (client === '__unknown__' ? item.client_id === null : item.client_id === client)) &&
    (project === 'all' || item.project_id === project) &&
    [item.project_id, item.name, item.client_id || 'sin clasificar']
      .join(' ').toLocaleLowerCase('es').includes(query));
}

export function localClientOptions(projects) {
  const ids = new Set(projects.map(project => project.client_id ?? '__unknown__'));
  return [...ids].sort((left, right) => left.localeCompare(right, 'es')).map(id => ({
    id, label: id === '__unknown__' ? 'Cliente sin clasificar' : id === 'internal' ? 'Interno' : id,
  }));
}
