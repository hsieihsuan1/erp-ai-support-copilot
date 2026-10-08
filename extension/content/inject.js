/* Demo-only replacement for the private source's automatic DOM capture. */
(() => {
  if (location.pathname !== '/demo/erp' || document.getElementById('erp-copilot-extension')) return;
  const host = document.createElement('div');
  host.id = 'erp-copilot-extension';
  const root = host.attachShadow({mode: 'open'});
  const button = document.createElement('button');
  button.textContent = 'Open ERP Support Copilot';
  button.style.cssText = 'position:fixed;right:28px;bottom:24px;background:#1748d4;color:white;border:0;border-radius:12px;padding:16px;font:600 15px system-ui;z-index:99999;cursor:pointer';
  root.append(button);
  let frame;
  button.addEventListener('click', () => {
    if (frame) { frame.remove(); frame = null; return; }
    frame = document.createElement('iframe');
    frame.title = 'ERP Support Copilot local demo';
    frame.src = 'http://127.0.0.1:8002/widget/widget.html';
    frame.style.cssText = 'position:fixed;right:24px;top:90px;width:450px;height:820px;border:1px solid #d4ddeb;border-radius:16px;z-index:99998;box-shadow:0 12px 48px #1b29442b;background:white';
    root.append(frame);
  });
  document.body.append(host);
  // Nothing is read from the ERP DOM or submitted without a user action.
})();
