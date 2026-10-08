const el = id => document.getElementById(id);
let session = null, transcript = [];
async function request(path, body) {
  const response = await fetch(path, {method: body ? 'POST' : 'GET', headers: {'Content-Type':'application/json', 'X-Demo-Identity':el('identity').value}, ...(body ? {body:JSON.stringify(body)} : {})});
  const data = await response.json();
  if (!response.ok) throw Error(typeof data.detail === 'string' ? data.detail : 'Invalid demo request');
  return data;
}
function bubble(role, text, sources, reason) {
  const div = document.createElement('div'); div.className = 'bubble ' + role;
  const title = document.createElement('h2'); title.textContent = role === 'user' ? 'Your reviewed message' : 'Synthetic runbook result'; div.append(title);
  const content = document.createElement('div'); content.textContent = text; div.append(content);
  if (sources) { const cite = document.createElement('div'); cite.className = 'source'; cite.textContent = 'Sources: ' + (sources.map(s => `${s.id} (${s.tenant})`).join(', ') || 'none'); div.append(cite); }
  if (reason) { const info = document.createElement('div'); info.className = 'reason'; info.textContent = reason; div.append(info); }
  el('conversation').append(div); div.scrollIntoView({block:'nearest'});
}
el('identity').addEventListener('change', () => {session=null; transcript=[];el('conversation').replaceChildren();el('transcript').textContent='No messages yet.';el('confirmed').checked=false;el('ticket').disabled=true;el('ticket-result').textContent='';});
el('confirmed').addEventListener('change', () => el('ticket').disabled = !session || !el('confirmed').checked);
el('chat').addEventListener('submit', async event => {
  event.preventDefault(); el('error').textContent=''; el('send').disabled=true;
  try {
    const message=el('message').value.trim();
    const data=await request('/api/chat', {message, module:el('module').value, session_id:session});
    session=data.session_id; const empty=document.querySelector('.empty');if(empty)empty.remove();
    bubble('user',message);bubble('assistant',data.message,data.sources,data.reason);
    transcript.push({role:'user',content:message},{role:'assistant',content:data.message});
    el('transcript').textContent=transcript.map(m=>m.role+': '+m.content).join('\n\n');
    el('confirmed').checked=false;el('ticket').disabled=true;
  } catch(error) {el('error').textContent=error.message;} finally {el('send').disabled=false;}
});
el('ticket').addEventListener('click', async () => {
  el('ticket').disabled=true; el('error').textContent='';
  try {const data=await request('/api/tickets',{session_id:session,provider:el('provider').value,confirmed:el('confirmed').checked});el('ticket-result').textContent=data.id+' - '+data.notice;}
  catch(error){el('error').textContent=error.message;}finally{el('ticket').disabled=!el('confirmed').checked;}
});
