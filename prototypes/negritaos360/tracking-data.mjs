// Synthetic product-planning examples, unrelated to actual projects or clients.
const features = [
  ['F-01', 'Contexto por proyecto', 'Mostrar cliente, responsable y alcance del proyecto.', []],
  ['F-02', 'Catálogo de capacidades', 'Buscar agents, skills y rules sin cruzar proyectos.', ['F-01']],
  ['F-03', 'Mapa de relaciones', 'Abrir una ficha desde un subgrafo de hasta tres saltos.', ['F-02']],
  ['F-04', 'Evidencia y procedencia', 'Toda validación muestra versión, criterio y referencia.', ['F-03']],
  ['F-05', 'Trazabilidad de trabajo', 'Relacionar tarea y commit sin importar diffs privados.', ['F-02']],
];

/** Build a fixture; execution evidence is deliberately separate from the spec. */
export function initialTrack(project) {
  const spec = {
    id: `${project}-v1`, project, version: '1.0', parentId: null,
    title: project === 'atlas' ? 'Un contexto fiable para cada decisión' : 'Un espacio de trabajo con trazabilidad',
    owner: 'Responsable de ejemplo', designRef: project === 'faro' ? null : 'UX-DEMO-01@1.0',
    goal: {
      id: `GOAL-${project.toUpperCase()}-01`,
      statement: 'Encontrar el contexto y su evidencia sin cambiar de herramienta.',
      metric: 'Tiempo mediano para encontrar contexto autorizado', target: 2, unit: 'min',
      direction: '≤', window: 'Primeras 10 sesiones del piloto', baseline: null, actual: null,
    },
    scope: 'Catálogo, relaciones y referencias de evidencia, en modo lectura.',
    exclusions: 'Sin ejecutar agentes, publicar datos ni modificar repositorios.',
    features: features.map(([id, name, criterion, dependencies]) => ({
      id, name, criterion, dependencies, owner: id === 'F-04' ? 'QA' : 'Frontend',
      acceptanceKey: `${project}:${id}:1`, designRef: 'UX-DEMO-01@1.0',
    })),
    change: { reason: 'Línea base inicial del ejemplo', kind: 'initial' },
  };
  return {
    project, revisions: [spec], activeId: project === 'atlas' ? spec.id : null,
    receipts: project === 'atlas' ? spec.features.slice(0, 2).map(f => ({
      id: `DEMO-${f.id}`, project, acceptanceKey: f.acceptanceKey,
      status: 'accepted', synthetic: true,
    })) : [],
    activations: project === 'atlas' ? [{ revisionId: spec.id, percent: 40, actor: 'Owner demo', sequence: 1 }] : [],
  };
}
