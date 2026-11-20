/* Pixling subpages: pixel wordmark with the live face in the i-dot, pixel arrows, stars.
   The sprite data is copied from src/page/src.html at build time (const WORD=['######...##...........##..##..................','#######..##...........##..##..................','##...##...............##......................','##...##..##..##...##..##..##..######....######','##...##..##..##...##..##..##..#######..#######','#######..##...##.##...##..##..##...##..##...##','######...##....###....##..##..##...##..##...##','##.......##...##.##...##..##..##...##..##...##','##.......##..##...##..##..##..##...##..#######','##.......##..##...##..##..##..##...##...######','............................................##','.......................................######.'];
const DOT={happy:P('11111111 11111111 11111111 11011011 10100101 11111111 11111111 11111111'),open:P('11111111 11111111 11011011 11011011 11011011 11111111 11111111 11111111'),half:P('11111111 11111111 11111111 11111111 11011011 11111111 11111111 11111111'),closed:P('11111111 11111111 11111111 11111111 10011001 11111111 11111111 11111111'),peek:P('11111111 11111111 01101111 01101111 01101111 11111111 11111111 11111111')};
const SEQ=[['happy',2400],['open',1600],['half',70],['closed',120],['half',70],['open',1400],['peek',1300],['open',900]];
const ARROW=['...#...','....#..','.....#.','#######','.....#.','....#..','...#...'];
const HEART=['.##.##.','#######','#######','.#####.','..###..','...#...'];
function wordBits(face){const f=DOT[face]||DOT.happy,o=[];for(let r=0;r<48;r++){let s='';for(let c=0;c<184;c++){let on=WORD[r>>2][c>>2]==='#';if(r<8&&c>=36&&c<44)on=f[r][c-36]==='1';s+=on?'1':'0';}o.push(s);}return o;}
function drawRows(cv,rows,fg,on='#'){cv.width=rows[0].length;cv.height=rows.length;const c=cv.getContext('2d');c.clearRect(0,0,cv.width,cv.height);c.fillStyle=fg;rows.forEach((r,y)=>{for(let x=0;x<r.length;x++)if(r[x]===on)c.fillRect(x,y,1,1);});}
function wordmark(cv){const fg=cv.dataset.fg,bit=Number(cv.dataset.bit)||1,u=Math.max(1,Math.round(bit*DPR));cv.width=184*u;cv.height=48*u;cv.style.width=184*u/DPR+'px';cv.style.height=48*u/DPR+'px';
  let i=0;const paint=()=>{const rows=wordBits(SEQ[i][0]),c=cv.getContext('2d');c.clearRect(0,0,cv.width,cv.height);c.fillStyle=fg;rows.forEach((r,y)=>{for(let x=0;x<184;x++)if(r[x]==='1')c.fillRect(x*u,y*u,u,u);});};
  const tick=()=>{i=(i+1)%SEQ.length;paint();setTimeout(tick,SEQ[i][1]);};paint();setTimeout(tick,SEQ[0][1]);}). */
(()=>{
const DPR=Math.max(1,Math.round(window.devicePixelRatio||1));
const P=s=>s.split(' ');
const WORD=['######...##...........##..##..................','#######..##...........##..##..................','##...##...............##......................','##...##..##..##...##..##..##..######....######','##...##..##..##...##..##..##..#######..#######','#######..##...##.##...##..##..##...##..##...##','######...##....###....##..##..##...##..##...##','##.......##...##.##...##..##..##...##..##...##','##.......##..##...##..##..##..##...##..#######','##.......##..##...##..##..##..##...##...######','............................................##','.......................................######.'];
const DOT={happy:P('11111111 11111111 11111111 11011011 10100101 11111111 11111111 11111111'),open:P('11111111 11111111 11011011 11011011 11011011 11111111 11111111 11111111'),half:P('11111111 11111111 11111111 11111111 11011011 11111111 11111111 11111111'),closed:P('11111111 11111111 11111111 11111111 10011001 11111111 11111111 11111111'),peek:P('11111111 11111111 01101111 01101111 01101111 11111111 11111111 11111111')};
const SEQ=[['happy',2400],['open',1600],['half',70],['closed',120],['half',70],['open',1400],['peek',1300],['open',900]];
const ARROW=['...#...','....#..','.....#.','#######','.....#.','....#..','...#...'];
const HEART=['.##.##.','#######','#######','.#####.','..###..','...#...'];
function wordBits(face){const f=DOT[face]||DOT.happy,o=[];for(let r=0;r<48;r++){let s='';for(let c=0;c<184;c++){let on=WORD[r>>2][c>>2]==='#';if(r<8&&c>=36&&c<44)on=f[r][c-36]==='1';s+=on?'1':'0';}o.push(s);}return o;}
function drawRows(cv,rows,fg,on='#'){cv.width=rows[0].length;cv.height=rows.length;const c=cv.getContext('2d');c.clearRect(0,0,cv.width,cv.height);c.fillStyle=fg;rows.forEach((r,y)=>{for(let x=0;x<r.length;x++)if(r[x]===on)c.fillRect(x,y,1,1);});}
function wordmark(cv){const fg=cv.dataset.fg,bit=Number(cv.dataset.bit)||1,u=Math.max(1,Math.round(bit*DPR));cv.width=184*u;cv.height=48*u;cv.style.width=184*u/DPR+'px';cv.style.height=48*u/DPR+'px';
  let i=0;const paint=()=>{const rows=wordBits(SEQ[i][0]),c=cv.getContext('2d');c.clearRect(0,0,cv.width,cv.height);c.fillStyle=fg;rows.forEach((r,y)=>{for(let x=0;x<184;x++)if(r[x]==='1')c.fillRect(x*u,y*u,u,u);});};
  const tick=()=>{i=(i+1)%SEQ.length;paint();setTimeout(tick,SEQ[i][1]);};paint();setTimeout(tick,SEQ[0][1]);}
document.querySelectorAll('#wordmark').forEach(wordmark);
document.querySelectorAll('canvas.px-arrow').forEach(cv=>drawRows(cv,ARROW,cv.dataset.fg||'#FCF8F0'));
document.querySelectorAll('canvas.px-heart').forEach(cv=>drawRows(cv,HEART,cv.dataset.fg||'#2F9083'));
document.querySelectorAll('.stars').forEach(st=>{const pts=[[6,10],[18,4],[30,22],[44,8],[71,6],[86,18],[93,40],[60,30],[12,46],[38,36],[80,52],[52,14]];
  pts.forEach((p,i)=>{const e=document.createElement('i');e.style.left=p[0]+'%';e.style.top=p[1]+'%';if(i%4===0)e.className='t';st.append(e);});});
})();
