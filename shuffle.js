// 🔀 Shuffle for tap-to-reveal term sheets (any page with #hide + table rows holding .ans)
// Adds "🔀 Shuffle" and "↩️ Order" next to Hide all. Rows shuffle within each table; Order restores.
(function(){
  if (document.getElementById('shuf')) return;          // page already has its own shuffle
  var hide = document.getElementById('hide'); if (!hide) return;
  var tables = [].slice.call(document.querySelectorAll('table')).filter(function(t){ return t.querySelector('.ans'); });
  if (!tables.length) return;
  var orig = tables.map(function(t){
    var rows = [].slice.call(t.querySelectorAll('tr')).filter(function(r){ return r.querySelector('.ans'); });
    return { parent: rows.length ? rows[0].parentNode : t, rows: rows };
  });
  function mk(id, label){ var b=document.createElement('button'); b.id=id; b.type='button'; b.textContent=label; hide.parentNode.insertBefore(b, hide.nextSibling); return b; }
  var ord = mk('order','↩️ Order'), shuf = mk('shuf','🔀 Shuffle');
  function hideAll(){ document.querySelectorAll('.ans.on').forEach(function(a){ a.classList.remove('on'); }); hide.click(); }
  shuf.onclick = function(){
    orig.forEach(function(o){
      var r = o.rows.slice();
      for (var i=r.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var x=r[i]; r[i]=r[j]; r[j]=x; }
      r.forEach(function(row){ o.parent.appendChild(row); });
    });
    hideAll();
  };
  ord.onclick = function(){ orig.forEach(function(o){ o.rows.forEach(function(row){ o.parent.appendChild(row); }); }); hideAll(); };
})();
