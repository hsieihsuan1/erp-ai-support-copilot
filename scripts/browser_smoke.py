"""Run the actual unpacked extension on a loopback server and capture evidence.
Run on Linux with: xvfb-run -a python scripts/browser_smoke.py
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).parents[1]
server=subprocess.Popen([sys.executable,'-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8002'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
try:
    for _ in range(100):
        try:
            if urlopen('http://127.0.0.1:8002/health').status==200:break
        except OSError:time.sleep(.1)
    else:raise RuntimeError('Demo server did not become ready')
    with sync_playwright() as p, tempfile.TemporaryDirectory() as profile:
        context=p.chromium.launch_persistent_context(profile,headless=False,channel='chromium',args=[f'--disable-extensions-except={ROOT / "extension"}',f'--load-extension={ROOT / "extension"}','--no-sandbox'],viewport={'width':1440,'height':1000})
        page=context.new_page();page.goto('http://127.0.0.1:8002/demo/erp')
        page.get_by_role('button',name='Open ERP Support Copilot').click()
        widget=page.frame_locator('iframe[title="ERP Support Copilot local demo"]')
        widget.get_by_role('button',name='Get runbook guidance').click()
        widget.get_by_text('Sources: alpha-ap-001 (alpha)',exact=True).wait_for()
        assert widget.locator('.bubble.assistant').count()==1
        assert 'beta review queue' not in widget.locator('#conversation').inner_text()
        widget.locator('summary').click()
        assert 'DEMO-AP-001' in widget.locator('#transcript').inner_text()
        assert 'Synthetic runbook guidance' in widget.locator('#transcript').inner_text()
        widget.locator('summary').click()
        widget.locator('#confirmed').check()
        widget.get_by_role('button',name='Create mock ticket').click()
        widget.get_by_text('MOCK-INC-0001 - Simulated locally. Nothing sent to ServiceNow or Jira.',exact=True).wait_for()
        # Expand viewport-contained iframe so the entire reviewed workflow fits in evidence.
        page.screenshot(path=str(ROOT/'docs/demo-running.png'),full_page=True)
        widget.locator('#provider').select_option('jira')
        widget.get_by_role('button',name='Create mock ticket').click()
        widget.get_by_text('MOCK-JIRA-0002 - Simulated locally. Nothing sent to ServiceNow or Jira.',exact=True).wait_for()
        widget.locator('#identity').select_option('beta-agent')
        widget.get_by_role('button',name='Get runbook guidance').click()
        widget.get_by_text('Sources: beta-ap-001 (beta)',exact=True).wait_for()
        assert 'alpha-ap-001' not in widget.locator('#conversation').inner_text()
        # HTML-like input is rendered as text, never interpreted as markup.
        widget.locator('#message').fill('<img src=x onerror="window.__demo_xss=true">')
        widget.get_by_role('button',name='Get runbook guidance').click()
        widget.get_by_text('Sources: none',exact=True).wait_for()
        assert not page.frames[-1].evaluate('Boolean(window.__demo_xss)')
        assert widget.locator('#conversation img').count()==0
        result={'browser':'Playwright Chromium with actual unpacked MV3 extension','extension_injection':True,'cited_alpha_runbook':True,'mock_servicenow':True,'mock_jira':True,'beta_fixture_isolated':True,'html_input_as_text':True,'url':page.url}
        (ROOT/'docs/browser-smoke.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result))
        context.close()
finally:
    server.terminate();server.wait(timeout=10)
