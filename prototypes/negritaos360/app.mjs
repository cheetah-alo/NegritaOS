import {navItems,projects,clients} from './data.mjs';
import {state,routeFromHash} from './state.mjs';
import {renderView} from './views.mjs';
import {showDetail} from './components.mjs';
import {resetTracking,tracking} from './tracking-view.mjs';
import {handleTrackingClick,bindTrackingForms} from './tracking-controller.mjs';
import {esc} from './components.mjs';
import {fetchLocalCatalog,localClientOptions} from './local-catalog.mjs';
import {renderLocalView} from './local-view.mjs';

const main=document.querySelector('#main');
const local={source:new URLSearchParams(location.search).get('source')==='local'?'local':'demo',
 status:'idle',projects:[],provenance:null,requestId:0};
document.querySelector('#client').insertAdjacentHTML('beforeend',clients.map(c=>`<option value="${c.id}">${c.name}</option>`).join(''));
function renderFilters(){
 const clientSelect=document.querySelector('#client'),projectSelect=document.querySelector('#project');
 const clientOptions=local.source==='local'?localClientOptions(local.projects):clients.map(c=>({id:c.id,label:c.name}));
 clientSelect.innerHTML=`<option value="all">${local.source==='local'?'Todos los clientes visibles':'Todos los clientes demo'}</option>`+
  clientOptions.map(c=>`<option value="${esc(c.id)}">${esc(c.label)}</option>`).join('');
 if(!clientOptions.some(c=>c.id===state.client))state.client='all';
 clientSelect.value=state.client;
 const available=local.source==='local'?local.projects.filter(p=>state.client==='all'||
  (state.client==='__unknown__'?p.client_id===null:p.client_id===state.client)).map(p=>({id:p.project_id,name:p.name})):
  projects.filter(p=>state.client==='all'||p.clientId===state.client);
 projectSelect.innerHTML=`<option value="all">${local.source==='local'?'Todos los proyectos visibles':'Todos los proyectos de ejemplo'}</option>`+
  available.map(p=>`<option value="${esc(p.id)}">${esc(p.name)}</option>`).join('');
 if(!available.some(p=>p.id===state.project))state.project='all';
 projectSelect.value=state.project;
}
function render(){
 document.querySelector('#nav').innerHTML=navItems.map(([id,name,icon])=>`<a href="#${id}" ${state.route===id?'aria-current="page"':''}><span aria-hidden="true">${icon}</span>${name}${state.route===id?'<i></i>':''}</a>`).join('');
 document.querySelector('#crumb').textContent=navItems.find(n=>n[0]===state.route)?.[1]||'Panorama';
 document.body.dataset.source=local.source;
 document.querySelector('#source').value=local.source;
 document.querySelector('#source-notice-title').textContent=local.source==='local'?'Catálogo local · lectura':'Prototipo interactivo';
 document.querySelector('#source-notice-text').textContent=local.source==='local'?
  'Sólo proyectos permitidos en este equipo. Otras secciones aún no están conectadas.':
  'Datos simulados. Sin conexión a Brain ni a repositorios.';
 document.querySelector('#reset').textContent=local.source==='local'?'Actualizar vista local ↺':'Restablecer demo ↺';
 renderFilters();
 document.querySelector('#scenario').value=state.scenario;
 document.querySelector('#scenario').disabled=local.source==='local';
 document.querySelector('#search').placeholder=local.source==='local'?'Buscar proyectos visibles…':
  state.route==='tracking'?'Buscar funcionalidades…':'Buscar en la vista…';
 main.innerHTML=local.source==='local'?renderLocalView(state.route,local,state):renderView();
}
async function loadLocal(){
 const request=++local.requestId;
 local.status='loading';render();
 try{
  const catalog=await fetchLocalCatalog();
  if(request!==local.requestId||local.source!=='local')return;
  Object.assign(local,{status:catalog.state,projects:catalog.projects,provenance:catalog.provenance});
 }catch{
  if(request!==local.requestId||local.source!=='local')return;
  Object.assign(local,{status:'error',projects:[],provenance:null});
 }
 render();
}
function setSource(value){
 local.source=value;local.requestId++;
 Object.assign(state,{client:'all',project:'all',search:'',scenario:'ready'});
 document.querySelector('#search').value='';
 const url=new URL(location.href);
 if(value==='local')url.searchParams.set('source','local');else url.searchParams.delete('source');
 history.replaceState(null,'',url.pathname+url.search+url.hash);
 if(value==='local')void loadLocal();else render();
}
function route(){state.route=routeFromHash(location.hash,state.route);state.kind='Todos';render();}
window.addEventListener('hashchange',route);
document.querySelector('#search').addEventListener('input',e=>{state.search=e.target.value;if(local.source==='demo'&&state.route==='tracking')tracking.tab='features';render();});
document.querySelector('#project').addEventListener('change',e=>{state.project=e.target.value;render();});
document.querySelector('#client').addEventListener('change',e=>{state.client=e.target.value;state.project='all';render();});
document.querySelector('#source').addEventListener('change',e=>setSource(e.target.value));
document.querySelector('#design').addEventListener('change',e=>{document.body.dataset.design=e.target.value;document.querySelector('#design-name').textContent=e.target.value==='tepulume'?'DISEÑO 02 / TEPULUME':'DISEÑO 01 / OBSERVATORIO';});
document.querySelector('#scenario').addEventListener('change',e=>{if(local.source==='demo'){state.scenario=e.target.value;render();}});
document.addEventListener('change',e=>{if(e.target.id==='depth'){state.depth=Number(e.target.value);render();}});
function reset(){Object.assign(state,{client:'all',project:'all',search:'',kind:'Todos',scenario:'ready',depth:3,zoom:1,step:0,graphMode:'capability'});document.querySelector('#search').value='';if(local.source==='local')void loadLocal();else{resetTracking();render();}}
document.querySelector('#reset').addEventListener('click',reset);
document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key==='k'){e.preventDefault();document.querySelector('#search').focus();}});
document.addEventListener('click',e=>{
 if(e.target.closest('a.skip')){e.preventDefault();main.focus();return;}
 const b=e.target.closest('button');if(!b)return;
 if(local.source==='local'){
  if(b.hasAttribute('data-local-retry')){void loadLocal();return;}
  if(b.hasAttribute('data-switch-demo')){setSource('demo');return;}
  if(b.hasAttribute('data-local-clear')){Object.assign(state,{client:'all',project:'all',search:''});document.querySelector('#search').value='';render();return;}
  if(b.dataset.route){location.hash=b.dataset.route;return;}
  if(b.dataset.project){state.project=b.dataset.project;location.hash='projects';render();}
  return;
 }
 if(handleTrackingClick(b,render))return;
 if(b.dataset.route)location.hash=b.dataset.route;
 if(b.dataset.project){state.project=b.dataset.project;location.hash='projects';render();}
 if(b.dataset.inspect)showDetail(b.dataset.inspect);
 if(b.hasAttribute('data-close'))document.querySelector('#detail').close();
 if(b.dataset.kind){state.kind=b.dataset.kind;render();}
 if(b.dataset.graph){state.graphMode=b.dataset.graph;render();}
 if(b.dataset.zoom){state.zoom=Math.min(1.45,Math.max(.7,Math.round((state.zoom+Number(b.dataset.zoom))*100)/100));render();}
 if(b.dataset.step!==undefined){state.step=Number(b.dataset.step);render();}
 if(b.hasAttribute('data-next')){state.step=(state.step+1)%5;render();}
 if(b.hasAttribute('data-retry')){state.scenario='ready';render();}
 if(b.hasAttribute('data-clear'))reset();
});
bindTrackingForms(render);
route();
if(local.source==='local')void loadLocal();
