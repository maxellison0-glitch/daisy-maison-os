const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const code = fs.readFileSync('./theme-changes/assets/dm-cart-extra-gifts.js','utf8');

async function scenario(outcome) {
  const button={disabled:false}, error={hidden:true}, inputs=[{dataset:{giftProperty:'Line 1'},value:' QA SECOND '}];
  const select={value:'501',selectedOptions:[{dataset:{title:'Large'}}]};
  const form={dataset:{root:'/',kind:'sign',title:'QA sign',bundle:'qa',parent:'existing-parent-key',failure:'Refresh your basket before trying again.'},reportValidity:()=>true,querySelector:s=>s==='button[type="submit"]'?button:s==='[data-gift-error]'?error:select,querySelectorAll:()=>inputs};
  let submit, added, destination;
  const window={DaisyCartSubmit:{create:()=>({add:async items=>{added=items;if(outcome)throw Object.assign(new Error('Uncertain basket'),outcome);}})},location:{assign:url=>{destination=url;}}};
  vm.runInNewContext(code,{window,document:{addEventListener:(name,fn)=>{submit=fn;}}});
  await submit({target:{closest:()=>form},preventDefault(){},stopImmediatePropagation(){}});
  return {added,destination,form,button,error};
}
(async()=>{
  const success=await scenario();
  assert.equal(success.added[0].parent_line_key,'existing-parent-key');
  assert.equal(success.added[0].properties['Line 1'],'QA SECOND');
  assert.equal(success.added[0].properties.Size,'Large');
  assert.equal(success.destination,'/cart');
  const uncertain=await scenario({reviewCart:true});
  assert.equal(uncertain.destination,undefined);
  assert.equal(uncertain.button.disabled,true);
  assert.equal(uncertain.form.dataset.busy,'true');
  assert.equal(uncertain.error.hidden,false);
  const rejected=await scenario({reviewCart:false});
  assert.equal(rejected.button.disabled,false);
  assert.equal(rejected.form.dataset.busy,'false');
  console.log('PASS: basket parent, personalisation, successful redirect, uncertain-response retry lock, explicit-rejection recovery.');
})().catch(error=>{console.error(error);process.exitCode=1;});
