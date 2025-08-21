document.addEventListener('DOMContentLoaded', () => {
  // Smooth fades for forms
  document.querySelectorAll('.card').forEach(c => {
    c.style.opacity = 0; 
    setTimeout(() => { 
      c.style.transition = 'opacity .3s'; 
      c.style.opacity = 1 
    }, 60);
  });

  // Interactive role buttons
  const roleButtons = document.querySelectorAll('.role-btn');
  if (roleButtons.length > 0) {
    // Add hover sound effect
    roleButtons.forEach(btn => {
      btn.addEventListener('mouseenter', () => {
        playHoverSound();
      });
      
      // Add click effect
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const href = btn.getAttribute('href');
        
        // Add click animation
        btn.classList.add('clicked');
        
        // Navigate after animation completes
        setTimeout(() => {
          window.location.href = href;
        }, 300);
      });
    });
  }
  
  // Simple sound effect function
  function playHoverSound() {
    // Create audio context on first interaction (to comply with browser policies)
    if (!window.audioContext) {
      window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    
    if (window.audioContext) {
      const oscillator = window.audioContext.createOscillator();
      const gainNode = window.audioContext.createGain();
      
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(1200, window.audioContext.currentTime);
      oscillator.frequency.exponentialRampToValueAtTime(600, window.audioContext.currentTime + 0.1);
      
      gainNode.gain.setValueAtTime(0.1, window.audioContext.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, window.audioContext.currentTime + 0.1);
      
      oscillator.connect(gainNode);
      gainNode.connect(window.audioContext.destination);
      
      oscillator.start();
      oscillator.stop(window.audioContext.currentTime + 0.1);
    }
  }
});
