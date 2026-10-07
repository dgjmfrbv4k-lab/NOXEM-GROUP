// usage: node record.js <config> frames <start> <end> <out.mp4> | stills t1,t2 <outdir> | sfx <out.json> | dur
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const {spawn}=require('child_process');const fs=require('fs');const path=require('path');
(async()=>{
  const [cfg,mode,a,b,c]=process.argv.slice(2);const fps=30;
  const br=await chromium.launch({args:['--allow-file-access-from-files']});
  const pg=await br.newPage({viewport:{width:1920,height:1080}});
  pg.on('pageerror',e=>console.error('PAGE ERROR',e.message));
  await pg.addInitScript({content:fs.readFileSync(path.join(__dirname,'configs',cfg+'.js'),'utf8')});
  await pg.goto('file://'+path.join(__dirname,'engine.html'));await pg.waitForFunction(()=>window.READY===true);
  if(mode==='dur'){console.log(await pg.evaluate(()=>window.DUR));}
  else if(mode==='sfx'){fs.writeFileSync(a,JSON.stringify(await pg.evaluate(()=>window.SFX)));}
  else if(mode==='stills'){for(const t of a.split(',').map(Number)){await pg.evaluate(t=>render(t),t);await pg.screenshot({path:path.join(b,`${cfg}_${t.toFixed(1)}.png`)});}}
  else{const f0=Math.round(+a*fps),f1=Math.round(+b*fps);
    const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','17','-preset','medium',c],{stdio:['pipe','inherit','inherit']});
    for(let f=f0;f<f1;f++){await pg.evaluate(t=>render(t),f/fps);const buf=await pg.screenshot({type:'png'});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
    ff.stdin.end();await new Promise(r=>ff.on('close',r));}
  await br.close();})();
