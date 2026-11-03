/* Swipe navigation for Study Mate decks (made by Claude).
   ← swipe left  = next card (reveals first if the answer isn't showing yet)
   → swipe right = previous card
   Ignores pinches, vertical scrolls, and swipes while a photo is zoomed. */
(function(){
  if(window.__swipe)return;window.__swipe=1;
  var sx=0,sy=0,lx=0,ly=0,st=0,multi=false,done=false;
  /* let the page own horizontal swipes (iOS otherwise steals them and fires touchcancel) */
  var css=document.createElement('style');css.textContent='html,body,.card,.pic,.pic img{touch-action:pan-y pinch-zoom}.zoom,.zoom img{touch-action:auto}#swipehint{font-size:12px;font-weight:800;color:#b0679a;margin-left:6px;white-space:nowrap}';document.head.appendChild(css);
  function hint(){var c=document.getElementById('count');if(c&&!document.getElementById('swipehint')){var h=document.createElement('span');h.id='swipehint';h.textContent='👆 swipe ← →';c.parentNode.insertBefore(h,c)}}
  if(document.readyState!=='loading')hint();else document.addEventListener('DOMContentLoaded',hint);
  function z(){var o=document.querySelector('.zoom.on');return !!o}
  function vis(id){var b=document.getElementById(id);return b&&b.offsetParent!==null?b:null}
  function cur(){return document.querySelector('.card.on')}
  function shown(c){if(!c)return true;if(c.classList.contains('open'))return true;
    var s=c.querySelectorAll('.stg');if(!s.length)return false;
    for(var i=0;i<s.length;i++)if(!s[i].classList.contains('vis'))return false;return true}
  function flash(t){var f=document.getElementById('swipeflash');
    if(!f){f=document.createElement('div');f.id='swipeflash';
      f.style.cssText='position:fixed;left:50%;top:45%;transform:translate(-50%,-50%);background:#6a3392e6;color:#fff;font:800 20px -apple-system,sans-serif;padding:10px 18px;border-radius:999px;z-index:99;pointer-events:none;transition:opacity .35s';
      document.body.appendChild(f)}
    f.textContent=t;f.style.opacity=1;clearTimeout(f._t);f._t=setTimeout(function(){f.style.opacity=0},450)}
  document.addEventListener('touchstart',function(e){multi=e.touches.length>1;if(multi)return;
    sx=lx=e.touches[0].clientX;sy=ly=e.touches[0].clientY;st=Date.now();done=false},{passive:true});
  document.addEventListener('touchmove',function(e){if(e.touches.length>1){multi=true;return}lx=e.touches[0].clientX;ly=e.touches[0].clientY},{passive:true});
  function end(x,y){
    if(done||multi||z())return;var dx=x-sx,dy=y-sy;
    if(Math.abs(dx)<50||Math.abs(dx)<Math.abs(dy)*1.2||Date.now()-st>1500)return;done=true;
    var b;
    if(dx<0){
      if(!shown(cur())){b=vis('reveal');if(b){b.click();flash('👀 Answer');return}}
      b=vis('skip')||vis('next');if(b){b.click();flash('Next ▶')}else flash('🎉 Last card')
    }else{
      b=vis('skipb')||vis('prev');if(b){b.click();flash('◀ Back')}
    }
  }
  document.addEventListener('touchend',function(e){var t=e.changedTouches[0];end(t.clientX,t.clientY)},{passive:true});
  document.addEventListener('touchcancel',function(){end(lx,ly)},{passive:true});
})();
