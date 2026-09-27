import { state } from './state.mjs';
import { esc } from './components.mjs';
import { tracking, currentTrack } from './tracking-view.mjs';
import { proposeRevision, activateRevision, validateFeature, featureState, progress } from './tracking-model.mjs';

function modal(title, body) {
  const dialog = document.querySelector('#detail');
  document.querySelector('#detail-content').innerHTML = `<div class="drawer-top"><span class="eyebrow">SEGUIMIENTO · DEMO</span><button class="icon-button" data-close aria-label="Cerrar detalle">×</button></div><h2 id="detail-title">${title}</h2>${body}<p id="track-error" role="alert"></p>`;
  if (!dialog.open) dialog.showModal();
}

/** Bind simulation controls only; no persistence, external writes or automation. */
export function handleTrackingClick(button, render) {
  if (button.dataset.trackProject) {
    state.project = button.dataset.trackProject; tracking.message = ''; render(); return true;
  }
  if (button.dataset.trackTab) { tracking.tab = button.dataset.trackTab; render(); return true; }
  const current = currentTrack();
  if (!current) return false;
  const { track, spec } = current;
  if (button.dataset.selectCandidate) {
    tracking.versions[track.project] = button.dataset.selectCandidate;
    tracking.tab = 'versions'; render(); return true;
  }
  if (button.hasAttribute('data-propose')) {
    modal('El cambio no borra el plan.', `<p class="drawer-summary">Crearás una revisión candidata de v${spec.version}. La línea base activa permanece intacta.</p><form id="propose-plan"><label>Qué cambia<select name="kind"><option value="add">Añadir una funcionalidad de ejemplo</option><option value="criterion">Cambiar el criterio de F-02</option></select></label><label>Motivo del cambio<textarea name="reason" required maxlength="280" placeholder="Ej.: necesitamos comparar el alcance entre versiones."></textarea></label><button class="button primary" type="submit">Crear revisión (demo)</button></form>`); return true;
  }
  if (button.hasAttribute('data-activate')) {
    const p = progress(track, spec);
    modal(`Activar v${spec.version}`, `<p class="drawer-summary">Revisa el contrato antes de cambiar la versión activa. Esta confirmación sólo afecta a la demo.</p><dl><dt>Objetivo</dt><dd>${esc(spec.goal.statement)}</dd><dt>Alcance</dt><dd>${spec.features.length} funcionalidades</dd><dt>Diseño</dt><dd>${esc(spec.designRef)}</dd><dt>Evidencia compatible</dt><dd>${p.done}/${p.total} · ${p.percent}% de entrega</dd><dt>Goal alcanzado</dt><dd>Desconocido, no medido</dd></dl><form id="activate-plan"><input type="hidden" name="revision" value="${spec.id}"><label class="check-label"><input type="checkbox" name="confirmed" required> He revisado objetivo, alcance, diseño y criterios de esta versión.</label><button class="button primary" type="submit">Confirmar activación (demo)</button></form>`); return true;
  }
  if (button.dataset.trackTask) {
    const f = spec.features.find(item => item.id === button.dataset.trackTask);
    if (!f) return false;
    const status = featureState(track, spec, f);
    modal(`${f.id} · ${esc(f.name)}`, `<span class="track-tag">${status} · demo</span><p class="drawer-summary">${esc(f.criterion)}</p><dl><dt>Cliente / proyecto</dt><dd>Ámbito ${esc(track.project)} · sintético</dd><dt>Goal</dt><dd>${esc(spec.goal.id)}</dd><dt>Diseño</dt><dd>${esc(f.designRef)}</dd><dt>Responsable</dt><dd>${esc(f.owner)}</dd><dt>Dependencias</dt><dd>${f.dependencies.join(', ') || 'Ninguna'}</dd><dt>Criterio versionado</dt><dd>${esc(f.acceptanceKey)}</dd><dt>Git</dt><dd>No conectado. Un commit no es una aceptación.</dd></dl><p class="annotation">Al simular, se añade evidencia ficticia; no se ejecutan tests reales ni se verifica el objetivo.</p><form id="validate-feature"><input type="hidden" name="revision" value="${spec.id}"><input type="hidden" name="feature" value="${f.id}"><button class="button primary" type="submit" ${status !== 'Pendiente' ? 'disabled' : ''}>Simular evidencia aceptada</button></form>`); return true;
  }
  return false;
}

export function bindTrackingForms(render) {
  document.addEventListener('change', event => {
    if (event.target.id !== 'plan-version') return;
    const { track } = currentTrack();
    tracking.versions[track.project] = event.target.value; tracking.message = ''; render();
  });
  document.addEventListener('submit', event => {
    if (!['propose-plan', 'activate-plan', 'validate-feature'].includes(event.target.id)) return;
    event.preventDefault();
    const data = new FormData(event.target);
    const { track } = currentTrack();
    try {
      if (event.target.id === 'propose-plan') {
        const revision = proposeRevision(track, data.get('kind'), data.get('reason'));
        tracking.versions[track.project] = revision.id; tracking.tab = 'versions';
        tracking.message = `Candidata v${revision.version} creada; la versión activa no cambia.`;
      } else if (event.target.id === 'activate-plan') {
        activateRevision(track, data.get('revision'), data.get('confirmed') === 'on');
        tracking.message = 'Activación simulada registrada. La versión anterior se conserva.';
      } else {
        validateFeature(track, data.get('revision'), data.get('feature'));
        tracking.message = 'Evidencia sintética aceptada. No es una validación real.';
      }
      document.querySelector('#detail').close(); render();
    } catch (error) {
      document.querySelector('#track-error').textContent = error.message;
    }
  });
}
