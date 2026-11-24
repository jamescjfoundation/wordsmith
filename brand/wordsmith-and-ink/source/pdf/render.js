const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const pg=await b.newPage();
for(const n of process.argv.slice(2)){await pg.goto('file://'+process.env.S+'/pdf/'+n+'.html');await pg.waitForLoadState('networkidle');await pg.evaluate(()=>document.fonts.ready);
await pg.evaluate(()=>{document.querySelectorAll('.pg').forEach((e,i,a)=>{const s=e.querySelector('.pn');if(s)s.textContent=(i+1)+' / '+a.length})});
await pg.pdf({path:process.env.S+'/pdf/'+n+'.pdf',width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});}
await b.close()})();
