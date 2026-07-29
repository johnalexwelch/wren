#!/usr/bin/env python3
"""Generate twin spike HTML files (cytoscape / sigma) with graph.json inlined."""
import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = (HERE / "graph.json").read_text()

COLORS = {"npc": "#e15759", "pc": "#f28e2b", "location": "#4e79a7", "organization": "#76b7b2",
          "artifact": "#edc948", "front": "#b07aa1", "event": "#59a14f"}

common_ui = """
<style>
 body{margin:0;font:13px system-ui;display:flex;height:100vh}
 #panel{width:230px;padding:10px;overflow:auto;border-right:1px solid #ccc;background:#fafafa}
 #graph{flex:1;position:relative}
 label{display:block;margin:2px 0}
 h3{margin:8px 0 4px;font-size:13px}
 .sw{display:inline-block;width:10px;height:10px;border-radius:5px;margin-right:4px}
 #info{position:absolute;top:8px;right:8px;background:#fffc;padding:6px 10px;border-radius:6px;max-width:320px;font-size:12px;pointer-events:none}
</style>
<div id="panel">
 <h3>Types</h3><div id="types"></div>
 <h3>Campaign</h3><div id="camps"></div>
 <h3>Edges</h3>
 <label><input type="checkbox" id="wiki" checked> wiki links (unlabeled)</label>
 <label><input type="checkbox" id="labeled" checked> labeled relationships</label>
 <h3>Focus</h3><div id="focushint">click a node to focus its neighborhood; click background to clear</div>
</div>
<div id="graph"><div id="info"></div></div>
"""

cyto = f"""<!doctype html><meta charset="utf8"><title>Warren graph spike — Cytoscape.js</title>
<script src="https://unpkg.com/cytoscape@3/dist/cytoscape.min.js"></script>
{common_ui}
<script>
const DATA={DATA};
const COLORS={json.dumps(COLORS)};
const elements=[
 ...DATA.nodes.map(n=>({{data:{{id:n.id,label:n.id,type:n.type,campaigns:n.campaigns.join('|')}}}})),
 ...DATA.edges.map((e,i)=>({{data:{{id:'e'+i,source:e.source,target:e.target,kind:e.kind,label:e.label||''}}}}))
];
const cy=cytoscape({{container:document.getElementById('graph'),elements,
 style:[
  {{selector:'node',style:{{'background-color':ele=>COLORS[ele.data('type')]||'#999','label':'data(label)','font-size':6,'width':10,'height':10,'color':'#333','text-opacity':0.7}}}},
  {{selector:'edge',style:{{'width':0.6,'line-color':'#ccc','curve-style':'haystack'}}}},
  {{selector:'edge[kind != "wiki"]',style:{{'width':1.6,'line-color':'#e15759','curve-style':'bezier','label':'data(label)','font-size':5,'text-rotation':'autorotate','text-opacity':0.9,'color':'#a33'}}}},
  {{selector:'.dim',style:{{'opacity':0.08,'text-opacity':0}}}},
  {{selector:'.hidden',style:{{'display':'none'}}}}
 ],
 layout:{{name:'cose',animate:false,nodeOverlap:8,idealEdgeLength:60}}}});
const t0=performance.now();
cy.ready(()=>{{document.getElementById('info').textContent=DATA.nodes.length+' nodes / '+DATA.edges.length+' edges — layout+render '+Math.round(performance.now()-t0)+'ms'}});
// filters
const types=[...new Set(DATA.nodes.map(n=>n.type))], camps=[...new Set(DATA.nodes.flatMap(n=>n.campaigns))];
const state={{types:new Set(types),camps:new Set(camps)}};
function boxes(el,items,set,colored){{items.forEach(v=>{{const l=document.createElement('label');
 l.innerHTML=(colored?'<span class="sw" style="background:'+(COLORS[v]||'#999')+'"></span>':'')+'<input type="checkbox" checked> '+v;
 l.querySelector('input').onchange=e=>{{e.target.checked?set.add(v):set.delete(v);apply()}};el.appendChild(l)}})}}
boxes(document.getElementById('types'),types,state.types,true);
boxes(document.getElementById('camps'),camps,state.camps,false);
document.getElementById('wiki').onchange=apply;document.getElementById('labeled').onchange=apply;
function apply(){{
 const wiki=document.getElementById('wiki').checked,lab=document.getElementById('labeled').checked;
 cy.batch(()=>{{
  cy.nodes().forEach(n=>{{const d=DATA.nodes.find(x=>x.id===n.id());
   const ok=state.types.has(d.type)&&(d.campaigns.length===0||d.campaigns.some(c=>state.camps.has(c)));
   n.toggleClass('hidden',!ok)}});
  cy.edges().forEach(e=>{{const k=e.data('kind');e.toggleClass('hidden',(k==='wiki'&&!wiki)||(k!=='wiki'&&!lab))}});
 }})}}
// focus
cy.on('tap','node',ev=>{{const n=ev.target;const hood=n.closedNeighborhood();
 cy.elements().addClass('dim');hood.removeClass('dim');
 document.getElementById('info').textContent=n.id()+' — '+n.degree()+' connections'}});
cy.on('tap',ev=>{{if(ev.target===cy)cy.elements().removeClass('dim')}});
</script>"""

sigma = f"""<!doctype html><meta charset="utf8"><title>Warren graph spike — sigma.js v3</title>
{common_ui}
<script type="module">
import Graph from "https://esm.sh/graphology@0.26.0";
import Sigma from "https://esm.sh/sigma@3.0.2";
import forceAtlas2 from "https://esm.sh/graphology-layout-forceatlas2@0.10.1";
const graphology={{Graph}};
const graphologyLibrary={{layoutForceAtlas2:forceAtlas2}};
const DATA={DATA};
const COLORS={json.dumps(COLORS)};
const g=new graphology.Graph({{multi:true}});
DATA.nodes.forEach(n=>g.addNode(n.id,{{label:n.id,size:3.5,color:COLORS[n.type]||'#999',x:Math.cos(g.order),y:Math.sin(g.order),node:n}}));
DATA.edges.forEach(e=>{{try{{g.addEdge(e.source,e.target,{{kind:e.kind,label:e.label||undefined,
 size:e.kind==='wiki'?0.5:1.6,color:e.kind==='wiki'?'#ccc':'#e15759'}})}}catch(_){{}}}});
graphologyLibrary.layoutForceAtlas2.assign(g,{{iterations:300,settings:graphologyLibrary.layoutForceAtlas2.inferSettings(g)}});
const t0=performance.now();
const state={{types:new Set(DATA.nodes.map(n=>n.type)),camps:new Set(DATA.nodes.flatMap(n=>n.campaigns)),wiki:true,lab:true,focus:null}};
const renderer=new Sigma(g,document.getElementById('graph'),{{renderEdgeLabels:true,edgeLabelSize:9,labelRenderedSizeThreshold:5,
 nodeReducer(node,data){{const n=data.node;let r={{...data}};
  const ok=state.types.has(n.type)&&(n.campaigns.length===0||n.campaigns.some(c=>state.camps.has(c)));
  if(!ok)r.hidden=true;
  if(state.focus&&node!==state.focus&&!g.areNeighbors(node,state.focus)){{r.color='#eee';r.label=null}}
  return r}},
 edgeReducer(edge,data){{let r={{...data}};const k=data.kind;
  if((k==='wiki'&&!state.wiki)||(k!=='wiki'&&!state.lab))r.hidden=true;
  if(state.focus&&!g.hasExtremity(edge,state.focus))r.hidden=true;
  return r}}}});
document.getElementById('info').textContent=DATA.nodes.length+' nodes / '+DATA.edges.length+' edges — FA2(300it)+first render '+Math.round(performance.now()-t0)+'ms';
const types=[...state.types],camps=[...state.camps];
function boxes(el,items,set,colored){{items.forEach(v=>{{const l=document.createElement('label');
 l.innerHTML=(colored?'<span class="sw" style="background:'+(COLORS[v]||'#999')+'"></span>':'')+'<input type="checkbox" checked> '+v;
 l.querySelector('input').onchange=e=>{{e.target.checked?set.add(v):set.delete(v);renderer.refresh()}};el.appendChild(l)}})}}
boxes(document.getElementById('types'),types,state.types,true);
boxes(document.getElementById('camps'),camps,state.camps,false);
document.getElementById('wiki').onchange=e=>{{state.wiki=e.target.checked;renderer.refresh()}};
document.getElementById('labeled').onchange=e=>{{state.lab=e.target.checked;renderer.refresh()}};
renderer.on('clickNode',({{node}})=>{{state.focus=node;renderer.refresh();
 document.getElementById('info').textContent=node+' — '+g.degree(node)+' connections'}});
renderer.on('clickStage',()=>{{state.focus=null;renderer.refresh()}});
window.renderer=renderer;window.g=g;window.state=state;
</script>"""

(HERE / "spike-cytoscape.html").write_text(cyto)
(HERE / "spike-sigma.html").write_text(sigma)
print("wrote spike-cytoscape.html", len(cyto)//1024, "KB; spike-sigma.html", len(sigma)//1024, "KB")
