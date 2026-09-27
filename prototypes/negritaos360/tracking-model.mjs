import { initialTrack } from './tracking-data.mjs';

/** Freeze plan definitions; observations remain separate append-only demo records. */
export function freezeSpec(value) {
  if (value && typeof value === 'object') {
    Object.values(value).forEach(freezeSpec);
    Object.freeze(value);
  }
  return value;
}

export function createTracks() {
  return Object.fromEntries(['atlas', 'brisa', 'faro'].map(id => {
    const track = initialTrack(id);
    track.revisions.forEach(freezeSpec);
    return [id, track];
  }));
}

export function accepted(track, feature) {
  if (!feature) return false;
  return track.receipts.some(r => r.project === track.project &&
    r.acceptanceKey === feature.acceptanceKey && r.status === 'accepted');
}

/** Equal-weight accepted functionality, never a proxy for goal achievement. */
export function progress(track, spec) {
  const total = spec.features.length;
  const done = spec.features.filter(f => accepted(track, f)).length;
  return { done, total, percent: total ? Math.round(100 * done / total) : null };
}

export function activationProblems(track, spec) {
  const issues = [];
  if (spec.project !== track.project) issues.push('Proyecto incompatible');
  if (!spec.owner) issues.push('Falta responsable');
  if (!spec.goal?.statement || !spec.goal?.metric || !Number.isFinite(spec.goal?.target) ||
      !spec.goal?.unit || !spec.goal?.window) issues.push('Objetivo no medible');
  if (!spec.designRef) issues.push('Falta diseño versionado');
  if (!spec.scope || !spec.exclusions) issues.push('Alcance incompleto');
  if (!spec.features.length) issues.push('Faltan funcionalidades');
  if (spec.features.some(f => !f.criterion || !f.owner || !f.designRef)) issues.push('Criterios incompletos');
  if (new Set(spec.features.map(f => f.id)).size !== spec.features.length) issues.push('IDs duplicados');
  if (spec.features.some(f => f.dependencies.some(id => !spec.features.some(d => d.id === id)))) {
    issues.push('Dependencia inexistente');
  }
  const pending = new Set(spec.features.map(f => f.id));
  while (pending.size) {
    const ready = spec.features.filter(f => pending.has(f.id) && f.dependencies.every(id => !pending.has(id)));
    if (!ready.length) { issues.push('Dependencias cíclicas'); break; }
    ready.forEach(f => pending.delete(f.id));
  }
  return issues;
}

export function featureState(track, spec, feature) {
  if (accepted(track, feature)) return 'Validada';
  if (!track.activeId || track.activeId !== spec.id) return 'Por validar';
  if (feature.dependencies.some(id => !accepted(track, spec.features.find(f => f.id === id)))) return 'Bloqueada';
  return 'Pendiente';
}

/** Create a candidate without modifying either the baseline or its old evidence. */
export function proposeRevision(track, kind, reason) {
  if (!track.activeId) throw new Error('Activa una línea base antes de proponer cambios.');
  if (track.revisions.some(r => r.id !== track.activeId && !track.activations.some(a => a.revisionId === r.id))) {
    throw new Error('Ya existe una revisión candidata.');
  }
  if (!reason.trim()) throw new Error('Indica el motivo del cambio.');
  if (!['add', 'criterion'].includes(kind)) throw new Error('Tipo de cambio no permitido.');
  const base = track.revisions.find(r => r.id === track.activeId);
  const next = structuredClone(base);
  const sequence = track.revisions.length + 1;
  Object.assign(next, { id: `${track.project}-v${sequence}`, version: `1.${sequence - 1}`,
    parentId: base.id, change: { kind, reason: reason.trim() } });
  if (kind === 'add') {
    const id = `F-${String(next.features.length + 1).padStart(2, '0')}`;
    next.features.push({ id, name: 'Comparación de versiones', owner: 'Frontend',
      criterion: 'Comparar alcance y avance sin sobrescribir la línea base anterior.',
      designRef: 'UX-DEMO-02@1.0', acceptanceKey: `${track.project}:${id}:${sequence}`, dependencies: ['F-02'] });
  } else {
    const feature = next.features.find(f => f.id === 'F-02');
    feature.criterion += ` Comprobar aislamiento por cliente (revisión ${sequence}).`;
    feature.acceptanceKey = `${track.project}:F-02:${sequence}`;
  }
  track.revisions.push(freezeSpec(next));
  return next;
}

export function activateRevision(track, revisionId, confirmed) {
  const spec = track.revisions.find(r => r.id === revisionId);
  if (!spec || !confirmed) throw new Error('Revisa y confirma la versión antes de activar.');
  if (track.activations.some(a => a.revisionId === revisionId)) throw new Error('Versión ya activada.');
  if (spec.parentId !== track.activeId) throw new Error('La versión activa ha cambiado.');
  const issues = activationProblems(track, spec);
  if (issues.length) throw new Error(issues.join(' · '));
  track.activeId = spec.id;
  track.activations.push({ revisionId, percent: progress(track, spec).percent,
    actor: 'Confirmación humana simulada', sequence: track.activations.length + 1 });
}

export function validateFeature(track, revisionId, featureId) {
  const spec = track.revisions.find(r => r.id === revisionId);
  const feature = spec?.features.find(f => f.id === featureId);
  if (!feature || track.activeId !== revisionId) throw new Error('Sólo se mide la versión activa.');
  if (featureState(track, spec, feature) !== 'Pendiente') throw new Error('La funcionalidad no está lista para validar.');
  track.receipts.push({ id: `DEMO-RECEIPT-${track.receipts.length + 1}`, project: track.project,
    acceptanceKey: feature.acceptanceKey, status: 'accepted', synthetic: true });
}
