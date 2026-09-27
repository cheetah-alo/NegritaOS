import {projects,clients,capabilities,knowledge} from "./data.mjs";
export const esc=value=>String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
export function badge(value){
 const tone={"Verificado":"ok","Desactualizado":"warn","Bloqueado":"bad","Revisar":"warn","Sin medir":"unknown","Sin verificar":"unknown"}[value]||"unknown";
 return `<span class="badge ${tone}"><span aria-hidden="true">●</span> ${esc(value)}</span>`;
}
export function heading(eyebrow,title,description,action=""){
 return `<div class="page-heading"><div><p class="eyebrow">${eyebrow}</p><h1>${title}</h1><p>${description}</p></div>${action}</div>`;
}
export const button=(text,route,kind="secondary")=>`<button class="button ${kind}" data-route="${route}">${text}</button>`;
export function empty(text="Prueba otro término o cambia el proyecto."){
 return `<div class="empty-state"><span class="empty-symbol">⌕</span><h2>No hay coincidencias</h2><p>${text}</p><button class="button secondary" data-clear>Limpiar filtros</button></div>`;
}
export function projectTable(items){
 if(!items.length)return empty();
 return `<div class="table-wrap"><table><thead><tr><th>Proyecto / enfoque</th><th>Cliente</th><th>Configuración</th><th>Capacidades</th><th>Responsable</th><th><span class="sr-only">Acción</span></th></tr></thead><tbody>${items.map(p=>`<tr><td><button class="project-link" data-project="${p.id}"><span class="project-icon" style="--project-color:${p.color}">${p.name[0]}</span><span><b>${p.name}</b><small>${p.area}</small></span></button></td><td>${esc(clients.find(c=>c.id===p.clientId)?.name||'Sin cliente')}</td><td>${badge(p.health)}</td><td>${capabilities.filter(c=>c.project===p.id).length}<span class="cell-muted"> definidas</span></td><td class="cell-muted">${p.owner}</td><td><button class="row-arrow" aria-label="Ver proyecto ${p.name}" data-project="${p.id}">↗</button></td></tr>`).join("")}</tbody></table></div>`;
}
export function capabilityTable(items){
 if(!items.length)return empty();
 return `<div class="table-wrap"><table><thead><tr><th>Capacidad</th><th>Tipo</th><th>Evidencia</th><th>Uso de ejemplo</th><th>Responsable</th></tr></thead><tbody>${items.map(c=>`<tr><td><button class="name-link" data-inspect="${c.id}">${esc(c.name)} <span>↗</span></button><small>${projects.find(p=>p.id===c.project)?.name||"Ejemplo"}</small></td><td><span class="type-label">${c.kind}</span></td><td>${badge(c.state)}</td><td>${c.use===null?'<span class="unknown-value">Sin medir</span>':c.use+' observaciones'}</td><td>${esc(c.owner||"Sin asignar")}</td></tr>`).join("")}</tbody></table></div>`;
}
export function showDetail(id){
 const item=[...capabilities,...knowledge,...projects].find(c=>c.id===id);
 if(!item)return;
 const dialog=document.querySelector("#detail");
 document.querySelector("#detail-content").innerHTML=`<div class="drawer-top"><span class="eyebrow">FICHA DE EJEMPLO</span><button class="icon-button" data-close aria-label="Cerrar detalle">×</button></div>
 <span class="detail-type">${item.kind||"Proyecto"}</span><h2 id="detail-title">${esc(item.name)}</h2>
 ${badge(item.state||item.health)}<p class="drawer-summary">${esc(item.note)}</p>
 <dl><dt>Cliente</dt><dd>${esc(clients.find(c=>c.id===(item.clientId||projects.find(p=>p.id===item.project)?.clientId))?.name||'Sin cliente')}</dd><dt>Responsable</dt><dd>${esc(item.owner||"Sin asignar")}</dd><dt>Definición</dt><dd>Registrada en la maqueta</dd>
 <dt>Evidencia</dt><dd>Simulada · no es una validación real</dd><dt>Uso observado</dt><dd>${item.use==null?"Desconocido. No equivale a cero.":item.use+" observaciones ficticias"}</dd><dt>Procedencia</dt><dd>Fixture local del prototipo</dd><dt>Clasificación</dt><dd>Demo · sin datos de cliente</dd></dl>
 <h3>Relaciones</h3>${(item.relations||[]).map(r=>`<button class="relation-link" data-inspect="${r}">${esc([...capabilities,...knowledge].find(c=>c.id===r)?.name||r)} <span>→</span></button>`).join("")||'<p class="muted">Sin relaciones declaradas en esta muestra.</p>'}
 <div class="drawer-foot">En el producto, esta ficha incluirá la versión y referencias de evidencia autorizadas.</div>`;
 if(!dialog.open)dialog.showModal();
}
