"""Conservative release checks, not proof that every secret pattern is known."""
from pathlib import Path
import re

root = Path(__file__).parents[1]
patterns = {
    'cloud identifier': r'ocid1\.[a-z]+\.',
    'Google API key': r'AIza[0-9A-Za-z_-]{30,}',
    'GitHub token': r'(?:ghp_|github_pat_)[0-9A-Za-z_]{20,}',
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    'email address': r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',
    'source personal domain': r'(?:level1\.|builder\.)?hsie\.com\.br',
}
findings=[];count=0
for path in root.rglob('*'):
    if not path.is_file() or any(x in path.parts for x in ['.git','__pycache__','.pytest_cache']):continue
    if path.suffix.lower() in {'.png','.zip'}:continue
    if path == Path(__file__):continue
    count+=1;text=path.read_text()
    for label,pattern in patterns.items():
        if re.search(pattern,text):findings.append(f'{path.relative_to(root)}: {label}')
    for url in re.findall(r'https?://[^\s<>"\x27)]+',text):
        if not url.startswith(('http://127.0.0.1:', 'http://localhost:', 'https://demo.', 'https://evil.example')):
            findings.append(f'{path.relative_to(root)}: non-demo URL requires review')
if (root/'.git').exists():findings.append('Unexpected imported git history')
print(f'Scanned {count} text files. Findings: {len(findings)}')
for result in findings:print(result)
raise SystemExit(bool(findings))
