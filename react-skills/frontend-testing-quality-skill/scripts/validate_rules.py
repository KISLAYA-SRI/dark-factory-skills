from pathlib import Path
import re
import yaml

REQUIRED = {'title', 'impact', 'impactDescription', 'tags'}

def parse_frontmatter(text: str) -> dict:
    if not text.startswith('---'):
        raise ValueError('missing frontmatter')
    end = text.index('---', 3)
    return yaml.safe_load(text[3:end]) or {}

def run_checks() -> int:
    rules_dir = Path('rules')
    if not rules_dir.exists():
        print('Missing rules directory')
        return 1
    errors = []
    for path in sorted(rules_dir.glob('*.md')):
        if path.name.startswith('_'):
            continue
        text = path.read_text(encoding='utf-8')
        try:
            fm = parse_frontmatter(text)
        except Exception as exc:
            errors.append(f'{path}: {exc}')
            continue
        missing = REQUIRED - set(fm)
        if missing:
            errors.append(f'{path}: missing {sorted(missing)}')
        if not re.search(r'\*\*Incorrect:\*\*', text):
            errors.append(f'{path}: missing Incorrect example')
        if not re.search(r'\*\*Correct:\*\*', text):
            errors.append(f'{path}: missing Correct example')
    if errors:
        print('\n'.join(errors))
        return 1
    print('Rule validation checks passed')
    return 0

if __name__ == '__main__':
    raise SystemExit(run_checks())