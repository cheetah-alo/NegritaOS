import {capabilities,projects,clients,navItems} from "./data.mjs";
export const state={route:"overview",client:'all',project:"all",search:"",kind:"Todos",scenario:"ready",depth:3,zoom:1,step:0};
export function projectInScope(project,s=state){
 return (!s.client||s.client==='all'||project.clientId===s.client)&&(s.project==='all'||project.id===s.project);
}
export function routeFromHash(hash,current='overview'){
 if(hash==='#main')return current;
 return navItems.some(n=>n[0]===hash.slice(1))?hash.slice(1):'overview';
}
export function selectCapabilities(s=state){
 const query=s.search.trim().toLocaleLowerCase("es");
 return capabilities.filter(c=>projectInScope(projects.find(p=>p.id===c.project),s)&&(s.kind==="Todos"||c.kind===s.kind)
 &&[c.name,c.kind,c.owner||"",c.note].join(" ").toLocaleLowerCase("es").includes(query));
}
export function selectProjects(s=state){
 const query=s.search.trim().toLocaleLowerCase("es");
 return projects.filter(p=>projectInScope(p,s)
 &&[p.name,p.area,p.owner,clients.find(c=>c.id===p.clientId)?.name||''].join(" ").toLocaleLowerCase("es").includes(query));
}
export function catalogMetrics(items){
 return {total:items.length,verified:items.filter(i=>i.state==="Verificado").length,
 attention:items.filter(i=>["Bloqueado","Desactualizado"].includes(i.state)).length,
 measured:items.filter(i=>i.use!==null).length};
}
export function neighborhood(root,edges,depth){
 const visible=new Set([root]);let frontier=[root];
 for(let hop=0;hop<depth;hop++){
  const next=[];for(const edge of edges)if(frontier.includes(edge.from)&&!visible.has(edge.to)){visible.add(edge.to);next.push(edge.to);}
  frontier=next;
 }
 return visible;
}
