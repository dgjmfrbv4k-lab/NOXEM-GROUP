const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1920,height:1080}});p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CERR',m.text())});
await p.goto('file://'+__dirname+'/test3d.html');await p.waitForFunction(()=>window.READY===true,null,{timeout:20000});
const shots=[
 ['f1',{set:'factory',t:3,cam:[-7,2.6,7],look:[0,1,0],fov:38}],
 ['f2',{set:'factory',t:6,cam:[-2,1.6,7.5],look:[-1,1.2,3],fov:35}],
 ['h1',{set:'house',install:1.2,night:0,people:1,cam:[10,4,18],look:[0,1.8,0]}],
 ['h2',{set:'house',install:6,night:0,people:4,cam:[6,3,16],look:[0,1.8,0]}],
 ['h3',{set:'house',install:6,night:1,people:4,cam:[-4,3,20],look:[0,2,0]}]];
for(const [n,s] of shots){const t0=Date.now();await p.evaluate(s=>shot(s),s);await p.screenshot({path:'stills_'+n+'.png'});console.log(n,Date.now()-t0,'ms');}
await b.close();})();
