import test from 'node:test';
import assert from 'node:assert/strict';
import {fetchLocalCatalog,parseLocalCatalog,selectLocalProjects,localClientOptions} from './local-catalog.mjs';
import {renderLocalView} from './local-view.mjs';

const digest='a'.repeat(64);
const response=projects=>({state:projects.length?'READY':'EMPTY',projects,
 provenance:{snapshot_id:'view-'+digest.slice(0,20),view_sha256:digest}});
const known={project_id:'alpha',name:'Alpha',client_id:'client_a',client_classification:'known'};
const unknown={project_id:'beta',name:'Beta',client_id:null,client_classification:'unknown'};

test('validates only allowlisted local catalog fields',()=>{
 assert.equal(parseLocalCatalog(response([known])).projects[0].name,'Alpha');
 assert.throws(()=>parseLocalCatalog(response([{...known,local_path:'/private/x'}])));
 assert.throws(()=>parseLocalCatalog(response([{...known,name:' '}])));
 assert.throws(()=>parseLocalCatalog({...response([]),state:'READY'}));
});
test('rejects client classification and repeated project IDs',()=>{
 assert.throws(()=>parseLocalCatalog(response([{...known,client_id:null}])));
 assert.throws(()=>parseLocalCatalog(response([known,known])));
});
test('filters only the already authorized input',()=>{
 const visible=parseLocalCatalog(response([known,unknown])).projects;
 assert.deepEqual(selectLocalProjects(visible,{client:'__unknown__'}).map(p=>p.project_id),['beta']);
 assert.deepEqual(selectLocalProjects(visible,{client:'client_a',project:'beta'}),[]);
 assert.deepEqual(selectLocalProjects(visible,{search:'ALPHA'}).map(p=>p.project_id),['alpha']);
 assert.deepEqual(localClientOptions(visible).map(option=>option.id),['__unknown__','client_a']);
});
test('fetches only the same-origin versioned endpoint',async()=>{
 let called;
  const result=await fetchLocalCatalog(async (url,options)=>{
    called={url,options};return {ok:true,json:async()=>response([known])};
  });
 assert.equal(called.url,'/api/v1/catalog');
 assert.equal(called.options.credentials,'same-origin');
 assert.equal(result.projects[0].project_id,'alpha');
 await assert.rejects(()=>fetchLocalCatalog(async()=>({ok:false})),/no disponible/);
});
test('local view escapes names and never renders synthetic metrics',()=>{
 const payload=response([{...known,name:'<script>alert(1)</script>'}]);
 const html=renderLocalView('overview',{...parseLocalCatalog(payload),status:'READY'},{});
 assert.match(html,/&lt;script&gt;/);
 assert.match(html,/data-route="catalog"/);
 assert.doesNotMatch(html,/<script>|8 observaciones|Atlas/);
  assert.match(
    renderLocalView('tracking',{status:'READY',projects:[],provenance:{snapshot_id:'view-a'}},{}),
    /todavía no está conectada/,
  );
});
test('local reading states stay distinct from demo scenarios',()=>{
 assert.match(renderLocalView('projects',{status:'loading'},{}),/Leyendo el catálogo autorizado/);
 assert.match(renderLocalView('projects',{status:'EMPTY'},{}),/No hay proyectos visibles/);
 assert.match(renderLocalView('projects',{status:'error'},{}),/Reintentar lectura/);
 assert.doesNotMatch(renderLocalView('projects',{status:'EMPTY'},{}),/Atlas|8 resultados de ejemplo/);
});
