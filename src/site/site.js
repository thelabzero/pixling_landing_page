/* Pixling subpages: pixel wordmark with the live face in the i-dot, pixel arrows, stars.
   The sprite data is copied from src/page/src.html at build time (/*BRAND*/). */
(()=>{
const DPR=Math.max(1,Math.round(window.devicePixelRatio||1));
const P=s=>s.split(' ');
/*BRAND*/
document.querySelectorAll('#wordmark').forEach(wordmark);
document.querySelectorAll('canvas.px-arrow').forEach(cv=>drawRows(cv,ARROW,cv.dataset.fg||'#FCF8F0'));
document.querySelectorAll('canvas.px-heart').forEach(cv=>drawRows(cv,HEART,cv.dataset.fg||'#2F9083'));
document.querySelectorAll('.stars').forEach(st=>{const pts=[[6,10],[18,4],[30,22],[44,8],[71,6],[86,18],[93,40],[60,30],[12,46],[38,36],[80,52],[52,14]];
  pts.forEach((p,i)=>{const e=document.createElement('i');e.style.left=p[0]+'%';e.style.top=p[1]+'%';if(i%4===0)e.className='t';st.append(e);});});
})();
