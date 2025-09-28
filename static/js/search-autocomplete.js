document.addEventListener('DOMContentLoaded', function(){
  const input = document.getElementById('global-search');
  const box = document.getElementById('autocomplete-box');
  if(!input || !box) return;

  let timer;
  input.addEventListener('input', function(e){
    clearTimeout(timer);
    timer = setTimeout(async ()=>{
      const q = e.target.value.trim();
      if(q.length < 2){ box.classList.add('hidden'); box.innerHTML=''; return; }
      try{
        const res = await fetch(`/api/search/?q=${encodeURIComponent(q)}`);
        if(!res.ok) { box.classList.add('hidden'); return; }
        const data = await res.json();
        let html = '';
        if(data.products && data.products.length){
          html += `<div class="p-2 border-b"><strong>محصولات</strong></div><ul>`;
          data.products.forEach(p => {
            html += `<li class="p-2 hover:bg-gray-100"><a class="block" href="${p.url}"><div class="text-sm font-medium">${p.name}</div><div class="text-xs text-gray-600">${p.excerpt||''}</div></a></li>`;
          });
          html += `</ul>`;
        }
        if(data.news && data.news.length){
          html += `<div class="p-2 border-t"><strong>اخبار</strong></div><ul>`;
          data.news.forEach(n => {
            html += `<li class="p-2 hover:bg-gray-100"><a class="block" href="${n.url}"><div class="text-sm">${n.title}</div></a></li>`;
          });
          html += `</ul>`;
        }
        box.innerHTML = html;
        box.classList.remove('hidden');
      }catch(err){
        box.classList.add('hidden');
      }
    }, 220);
  });

  document.addEventListener('click', (ev)=>{ if(!box.contains(ev.target) && ev.target!==input) box.classList.add('hidden'); });
});
