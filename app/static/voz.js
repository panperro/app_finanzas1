// Reconocimiento de voz básico para completar inputs
window.addEventListener('DOMContentLoaded', () => {
  if (!('webkitSpeechRecognition' in window)) return;

  const micBtn = document.createElement('button');
  micBtn.textContent = '🎙️ Dictar';
  micBtn.style.marginLeft = '1rem';
  document.querySelector('header')?.appendChild(micBtn);

  const recog = new webkitSpeechRecognition();
  recog.lang = 'es-ES';
  recog.onresult = e => {
    const texto = e.results[0][0].transcript;
    const activo = document.activeElement;
    if (activo && activo.tagName === 'INPUT') {
      activo.value = texto;
    }
  };

  micBtn.addEventListener('click', () => recog.start());
});