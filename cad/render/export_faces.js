// Exports wedge face bitmaps to faces.json (run from project root: node cad/render/export_faces.js)
const fs=require('fs');const t=fs.readFileSync('references/Dino Wedge Sheet.html','utf8');
const sc=[...t.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
eval(sc[0]+';globalThis.build=build;');
const g=build('10:24','SAM');const all={};g.forEach(G=>G.scenes.forEach(s=>all[s.key]=s));
const out={idle:all.expressions.frames[0][0],happy:all.expressions.frames[1][0],love:all.expressions.frames[2][0],mischief:all.expressions.frames[12][0],excited:all.expressions.frames[15][0]};
all.time.frames.forEach((f,i)=>out['time'+i]=f[0]);
const o={};for(const k in out)o[k]=Array.from(out[k]).join('');fs.writeFileSync('cad/render/faces/faces.json',JSON.stringify(o));
