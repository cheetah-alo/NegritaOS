const ITEM_KEYS = ['id', 'project_id', 'kind', 'name', 'configuration_state'];
const TOP_LEVEL_KEYS = ['state', 'items', 'provenance'];
const PROVENANCE_KEYS = ['snapshot_id', 'view_sha256'];
const KINDS = new Set(['agent', 'skill', 'rule']);
const CONFIGURATION_STATES = new Set(['REGISTERED', 'RESOLVED', 'DECLARED']);
const HASH = /^[0-9a-f]{64}$/;

function hasExactKeys(value, keys) {
  return value && typeof value === 'object' && !Array.isArray(value) &&
    Object.keys(value).sort().join(',') === [...keys].sort().join(',');
}

function requiredText(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

export function parseLocalCapabilities(payload) {
  if (!hasExactKeys(payload, TOP_LEVEL_KEYS) || !['READY', 'EMPTY'].includes(payload.state) ||
      !Array.isArray(payload.items) || !hasExactKeys(payload.provenance, PROVENANCE_KEYS)) {
    throw new Error('Contrato de capacidades locales inválido');
  }

  const {snapshot_id: snapshotId, view_sha256: viewSha256} = payload.provenance;
  if (!requiredText(snapshotId) || !HASH.test(viewSha256)) {
    throw new Error('Procedencia de capacidades locales inválida');
  }

  const seen = new Set();
  const items = payload.items.map(item => {
    const identity = `${item?.project_id}\u0000${item?.kind}\u0000${item?.id}`;
    if (!hasExactKeys(item, ITEM_KEYS) || !requiredText(item.id) || seen.has(identity) ||
        !requiredText(item.project_id) || !KINDS.has(item.kind) || !requiredText(item.name) ||
        !CONFIGURATION_STATES.has(item.configuration_state)) {
      throw new Error('Elemento de capacidades locales inválido');
    }
    seen.add(identity);
    return {
      id: item.id,
      project_id: item.project_id,
      kind: item.kind,
      name: item.name.trim(),
      configuration_state: item.configuration_state,
    };
  });

  if ((payload.state === 'EMPTY') !== (items.length === 0)) {
    throw new Error('Estado de capacidades locales inconsistente');
  }

  return {
    state: payload.state,
    items,
    provenance: {snapshot_id: snapshotId, view_sha256: viewSha256},
  };
}

export async function fetchLocalCapabilities(fetcher = fetch, filters = {}) {
  const params = new URLSearchParams();
  if (typeof filters.project === 'string' && filters.project.trim()) {
    params.set('project_id', filters.project.trim());
  }
  if (KINDS.has(filters.kind)) params.set('kind', filters.kind);
  const query = params.toString();
  const url = `/api/v1/capabilities${query ? `?${query}` : ''}`;
  const response = await fetcher(url, {
    method: 'GET', cache: 'no-store', credentials: 'same-origin',
    headers: {Accept: 'application/json'},
  });
  if (!response.ok) throw new Error('Capacidades locales no disponibles');
  return parseLocalCapabilities(await response.json());
}

export function selectLocalCapabilities(items, {project = 'all', kind = 'all', search = ''} = {}) {
  if (!Array.isArray(items)) return [];
  const query = String(search).trim().toLocaleLowerCase('es');
  return items.filter(item =>
    (project === 'all' || item.project_id === project) &&
    (kind === 'all' || item.kind === kind) &&
    [item.id, item.project_id, item.kind, item.name, item.configuration_state]
      .join(' ').toLocaleLowerCase('es').includes(query));
}
