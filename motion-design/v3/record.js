// usage: node record.js frames <start> <end> <out.mp4>  |  node record.js stills t1,t2,... <outdir>  |  node record.js sfx [sfx.json]
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const {spawn}=require('child_process');
const path=require('path');
(async()=>{
  const [mode,a,b,c]=process.argv.slice(2);
  const fps=30;
  const br=await chromium.launch({args:['--allow-file-access-from-files']});
  const pg=await br.newPage({viewport:{width:1920,height:1080}});
  pg.on('pageerror',e=>console.error('PAGE ERROR',e));
  await pg.goto('file://'+path.join(__dirname,'index.html'));
  await pg.waitForFunction(()=>window.READY===true);
  if(mode==='sfx'){
    require('fs').writeFileSync(a||'sfx.json',JSON.stringify(await pg.evaluate(()=>window.SFX)));
  } else if(mode==='stills'){
    for(const t of a.split(',').map(Number)){
      await pg.evaluate(t=>render(t),t);
      await pg.screenshot({path:path.join(b,`t${t.toFixed(2)}.png`)});
    }
  } else {
    const f0=Math.round(+a*fps), f1=Math.round(+b*fps);
    const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-',
      '-c:v','libx264','-pix_fmt','yuv420p','-crf','16','-preset','medium',c],{stdio:['pipe','inherit','inherit']});
    for(let f=f0;f<f1;f++){
      await pg.evaluate(t=>render(t),f/fps);
      const buf=await pg.screenshot({type:'png'});
      if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
    }
    ff.stdin.end(); await new Promise(r=>ff.on('close',r));
  }
  await br.close();
})();
