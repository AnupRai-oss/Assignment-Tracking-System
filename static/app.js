async function fetchAssignments(){
  const res = await fetch('/api/assignments');
  return await res.json();
}

function render(list){
  const ul = document.getElementById('list');
  ul.innerHTML = '';
  list.forEach(a => {
    const li = document.createElement('li');
    li.className = 'item';
    const due = a.due_date ? ` (due ${a.due_date})` : '';
    li.innerHTML = `<div class="main"><strong>${escape(a.title)}</strong>${due}<div class="desc">${escape(a.description || '')}</div></div>`;

    const actions = document.createElement('div');
    actions.className = 'actions';

    const doneBtn = document.createElement('button');
    doneBtn.textContent = a.status === 'done' ? 'Undo' : 'Done';
    doneBtn.onclick = async () => {
      await fetch(`/api/assignments/${a.id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify({status: a.status === 'done' ? 'pending' : 'done'})});
      load();
    };

    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.onclick = async () => { if(confirm('Delete this assignment?')){ await fetch(`/api/assignments/${a.id}`, {method:'DELETE'}); load(); }};

    actions.appendChild(doneBtn);
    actions.appendChild(delBtn);
    li.appendChild(actions);
    ul.appendChild(li);
  });
}

function escape(s){
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

async function load(){
  const list = await fetchAssignments();
  render(list);
}

document.getElementById('addForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const title = document.getElementById('title').value.trim();
  const due = document.getElementById('due_date').value || null;
  const description = document.getElementById('description').value.trim();
  if(!title) return alert('Title required');
  await fetch('/api/assignments', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({title, due_date: due, description})});
  document.getElementById('addForm').reset();
  load();
});

load();
