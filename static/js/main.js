(function () {
  'use strict';

  const form       = document.getElementById('predictionForm');
  const submitBtn  = document.getElementById('submitBtn');
  const loadingBar = document.getElementById('loadingBar');
  const loadingTxt = document.getElementById('loadingText');

  // ── Form submit -  show loading state ──────────────────────
  form.addEventListener('submit', function () {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing...';
    loadingBar.classList.add('active');
    loadingTxt.classList.add('active');
  });

  // ── Toggle label state sync ────────────────────────────────
  document.querySelectorAll('.toggle-switch input').forEach(function (cb) {
    const label = cb.closest('.toggle-group')?.querySelector('.toggle-label');
    if (!label) return;

    function sync() {
      label.textContent = cb.checked ? 'Yes' : 'No';
    }

    sync();
    cb.addEventListener('change', sync);
  });

  // ── Scroll to result on page load ─────────────────────────
  const result = document.querySelector('.result-panel');
  if (result) {
    requestAnimationFrame(function () {
      result.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
})();
