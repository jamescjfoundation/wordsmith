// Renders brand.html and products.html (made by brand.py and products.py) to PDF. Run through build.py --pdf.
const {chromium}=require('playwright');const OUT=process.env.WORDSMITH_PDF_OUT;
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const pg=await b.newPage();
for(const n of process.argv.slice(2)){await pg.goto('file://'+OUT+'/'+n+'.html');await pg.waitForLoadState('networkidle');await pg.evaluate(()=>document.fonts.ready);
await pg.evaluate(()=>{document.querySelectorAll('.pg').forEach((e,i,a)=>{const s=e.querySelector('.pn');if(s)s.textContent=(i+1)+' / '+a.length})});
await pg.pdf({path:OUT+'/'+n+'.pdf',width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});}
await b.close()})();
