import {capabilities,knowledge,projects} from './data.mjs';
import {state,neighborhood,projectInScope} from './state.mjs';
import {esc} from './components.mjs';

export function graph(mode='capability') {
  const root={id:'ecosystem',name:'Mi ecosistema',kind:'Contexto'};
  const projectNodes=projects.filter(p=>projectInScope(p)).map(p=>({...p,kind:'Proyecto'}));
  const leaves=(mode==='knowledge'?knowledge:capabilities).filter(c=>projectNodes.some(p=>p.id===c.project));
  const edges=[...projectNodes.map(p=>({from:root.id,to:p.id})),...leaves.filter(c=>mode==='knowledge'?c.id==='knowledge-question':c.kind==='Agent').map(c=>({from:c.project,to:c.id})),...leaves.flatMap(c=>c.relations.map(id=>({from:c.id,to:id})))];
  // Count useful relationship hops from a project, not from the decorative root.
  const visible=new Set([root.id,...projectNodes.flatMap(p=>[...neighborhood(p.id,edges,state.depth)])]);
  const query=state.search.toLowerCase();
  const nodes=[root,...projectNodes,...leaves].filter(n=>visible.has(n.id));
  const positions=new Map([[root.id,{x:108,y:190}]]);
  projectNodes.forEach((n,i)=>positions.set(n.id,{x:310,y:80+i*115}));
  leaves.forEach((n,i)=>positions.set(n.id,{x:520+(i%2)*200,y:45+Math.floor(i/2)*91}));
  if(mode==='knowledge') leaves.forEach((n,i)=>positions.set(n.id,{x:480+i*155,y:100+i*95}));
  const line=edges.filter(e=>nodes.some(n=>n.id===e.from)&&nodes.some(n=>n.id===e.to)).map(e=>{const a=positions.get(e.from),b=positions.get(e.to);return `<path d="M${a.x},${a.y} C${(a.x+b.x)/2},${a.y} ${(a.x+b.x)/2},${b.y} ${b.x},${b.y}"/>`;}).join('');
  const marks=nodes.map(n=>{const p=positions.get(n.id),hit=!query||n.name.toLowerCase().includes(query);return `<g transform="translate(${p.x} ${p.y})" class="graph-node ${n.kind==='Proyecto'?'project-node':''} ${hit?'':'dim'}"><circle r="${n.id===root.id?27:18}"/><text y="5" class="node-glyph">${n.id===root.id?'n·':n.kind==='Proyecto'?n.name[0]:'·'}</text><text y="37" class="node-title">${esc(n.name.length>25?n.name.slice(0,23)+'…':n.name)}</text><text y="52" class="node-kind">${n.kind}</text></g>`;}).join('');
  return `<div class="graph-stage"><svg viewBox="0 0 900 430" role="img" aria-label="Relaciones de ejemplo; lista navegable debajo"><g transform="translate(${450*(1-state.zoom)} ${215*(1-state.zoom)}) scale(${state.zoom})"><g class="graph-lines">${line}</g>${marks}</g></svg><span class="graph-caption">RELACIONES DECLARADAS · NO SIMILITUD INFERIDA</span></div>
  <div class="graph-node-list" aria-label="Nodos del grafo">${nodes.filter(n=>n.id!=='ecosystem'&&(!query||n.name.toLowerCase().includes(query))).map(n=>`<button data-inspect="${n.id}" class="node-chip"><span class="tiny-dot"></span>${esc(n.name)}</button>`).join('')||'<span class="muted">No hay nodos que coincidan.</span>'}</div>`;
}
