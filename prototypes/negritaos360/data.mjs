// Synthetic fixtures only. No filesystem, account, memory or repository reads.
export const clients = [
 {id:'client-a',name:'Cliente demo A'}, {id:'client-b',name:'Cliente demo B'},
];
export const projects = [
 {id:"atlas",clientId:'client-a',name:"Atlas",area:"Analítica operativa",owner:"Equipo de datos",color:"#0d6684",health:"Revisar",note:"Una regla cambió después de la última verificación."},
 {id:"brisa",clientId:'client-a',name:"Brisa",area:"Producto y experiencia",owner:"Equipo de producto",color:"#a81256",health:"Verificado",note:"Configuración de ejemplo resuelta; uso aún sin instrumentar."},
 {id:"faro",clientId:'client-b',name:"Faro",area:"Investigación aplicada",owner:"Equipo de investigación",color:"#8a5a08",health:"Sin medir",note:"Faltan observaciones para evaluar su utilización."},
];
export const capabilities = [
 {id:"agent-architect",name:"Arquitectura de software",kind:"Agent",project:"atlas",owner:"Arquitectura",state:"Verificado",use:null,note:"Define responsabilidades y contratos antes de implementar.",relations:["skill-contract","skill-quality"]},
 {id:"skill-contract",name:"Contratos de datos",kind:"Skill",project:"atlas",owner:"Datos",state:"Verificado",use:3,note:"Valida estructura, claves y estados explícitos.",relations:["rule-evidence"]},
 {id:"skill-quality",name:"Testing y cobertura",kind:"Skill",project:"atlas",owner:"Calidad",state:"Verificado",use:2,note:"Convierte los criterios de aceptación en evidencia reproducible.",relations:["rule-evidence"]},
 {id:"rule-evidence",name:"Evidencia antes de aprobar",kind:"Rule",project:"atlas",owner:"Gobierno",state:"Desactualizado",use:null,note:"Ejemplo de regla modificada: los resultados anteriores requieren revalidación.",relations:[]},
 {id:"agent-reviewer",name:"Revisión independiente",kind:"Agent",project:"brisa",owner:"Calidad",state:"Verificado",use:4,note:"Contrasta el resultado con los criterios aceptados.",relations:["skill-interface"]},
 {id:"skill-interface",name:"Diseño de interfaz",kind:"Skill",project:"brisa",owner:"Experiencia",state:"Verificado",use:null,note:"Mantiene navegación, contraste y estados conectados.",relations:[]},
 {id:"agent-research",name:"Asesoría de investigación",kind:"Agent",project:"faro",owner:"Investigación",state:"Sin verificar",use:null,note:"Relaciona preguntas, fuentes y decisiones. No hay evidencia de uso.",relations:["skill-sources"]},
 {id:"skill-sources",name:"Revisión de fuentes",kind:"Skill",project:"faro",owner:null,state:"Bloqueado",use:null,note:"Ejemplo de dependencia sin responsable asignado.",relations:[]},
];
export const knowledge = [
 {id:"knowledge-question",name:"¿Qué respalda esta decisión?",kind:"Pregunta",project:"atlas",owner:"Datos",state:"Sin verificar",use:null,note:"Consulta de ejemplo: recorre relaciones explícitas hasta la evidencia.",relations:["knowledge-decision"]},
 {id:"knowledge-decision",name:"Contratos tipados",kind:"Decisión",project:"atlas",owner:"Arquitectura",state:"Verificado",use:null,note:"Decisión sintética enlazada a una comprobación; no representa una aprobación real.",relations:["knowledge-evidence"]},
 {id:"knowledge-evidence",name:"Receipt de validación",kind:"Evidencia",project:"atlas",owner:"Calidad",state:"Verificado",use:null,note:"Referencia ficticia al resultado que sustentaría la decisión.",relations:[]},
];
export const workflowSteps=[
 {name:"Planificar",role:"Responsable",detail:"Definir resultado, límites y criterios de aceptación."},
 {name:"Preparar",role:"Worker",detail:"Cargar sólo el contexto necesario para la tarea."},
 {name:"Comprobar",role:"Revisor independiente",detail:"Intentar refutar el resultado y adjuntar evidencia."},
 {name:"Decidir",role:"Owner humano",detail:"Autorizar la acción si corresponde. Aquí sólo simulamos la navegación."},
 {name:"Entregar",role:"Handoff",detail:"Guardar referencias y siguientes pasos, sin replicar contenido privado."},
];
export const navItems=[
 ["overview","Panorama","◉"],["projects","Proyectos","▦"],["tracking","Planes y avance","↗"],["agents","Agentes","◈"],["catalog","Capacidades","▤"],
 ["knowledge","Conocimiento","⌘"],["flows","Flujos de trabajo","⇢"],["brain","Brain y Git","◎"],
];
