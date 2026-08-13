from pathlib import Path
import os

def run_checks() -> int:
    required_files = [
        Path('SKILL.md'),
        Path('AGENTS.md'),
        Path('rules/_sections.md'),
        Path('rules/_template.md'),
        Path('test-cases.json')
    ]
    missing = [str(p) for p in required_files if not p.exists()]
    if missing:
        print('Missing required references:', ', '.join(missing))
        return 1

    required_env = []
    missing_env = [name for name in required_env if not os.environ.get(name)]
    if missing_env:
        print('Missing required environment variables:', ', '.join(missing_env))
        return 1

    print('Validation checks passed')
    return 0

if __name__ == '__main__':
    raise SystemExit(run_checks())