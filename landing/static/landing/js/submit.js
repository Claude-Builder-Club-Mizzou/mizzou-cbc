/* Submit page: post the form in the background so a validation error never reloads the page.
   A reload would wipe the chosen files (browsers can't refill file inputs), so on an error we
   swap in only the server's error box and leave every field exactly as the user left it.
   Without JS the form still posts normally. */
(function () {
  const form = document.querySelector('.submit-form');
  if (!form || !window.fetch || !window.FormData || !window.DOMParser) return;

  const button = form.querySelector('button[type="submit"]');
  const label = button ? button.textContent : '';

  function setBusy(busy) {
    if (!button) return;
    button.disabled = busy;
    button.textContent = busy ? 'Submitting…' : label;
  }

  function showErrors(html) {
    const incoming = new DOMParser().parseFromString(html, 'text/html').querySelector('.submit-errors');
    const current = form.parentElement.querySelector('.submit-errors');
    if (current) current.remove();
    if (!incoming) return false;
    form.parentElement.insertBefore(incoming, form);
    incoming.setAttribute('tabindex', '-1');
    incoming.scrollIntoView({ behavior: 'smooth', block: 'center' });
    incoming.focus({ preventScroll: true });
    return true;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (button && button.disabled) return; // already sending: no duplicate submissions
    setBusy(true);
    try {
      const res = await fetch(form.action || window.location.href, {
        method: 'POST',
        body: new FormData(form),
        credentials: 'same-origin',
      });
      if (res.redirected) {
        window.location.href = res.url; // saved: on to the thank-you page
        return;
      }
      const html = await res.text();
      if (res.ok && showErrors(html)) {
        setBusy(false);
        return;
      }
      throw new Error('Unexpected response');
    } catch (err) {
      // Don't re-post on our own: the first request may have saved before the connection dropped.
      // Keep the form as-is and let the user retry.
      showErrors('<div class="submit-errors" role="alert"><strong>Something went wrong sending your project.</strong> Check your connection and press Submit again. Your answers and files are still here.</div>');
      setBusy(false);
    }
  });
})();
