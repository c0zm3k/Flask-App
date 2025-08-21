document.addEventListener('DOMContentLoaded', () => {
  // Smooth fades for forms
  document.querySelectorAll('.card').forEach(c=>{
    c.style.opacity=0; setTimeout(()=>{ c.style.transition='opacity .3s'; c.style.opacity=1 }, 60)
  });
});
