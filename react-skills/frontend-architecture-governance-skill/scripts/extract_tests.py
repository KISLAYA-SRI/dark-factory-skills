from pathlib import Path
import json
import re
import yaml

def frontmatter(text: str) -> dict:
    if not text.startswith('---'):
        return {}
    end = text.index('---', 3)
    return yaml.safe_load(text[3:end]) or {}

def compact(value: str, limit: int = 360) -> str:
    value = re.sub(r'\s+', ' ', value).strip()
    return value if len(value) <= limit else value[: limit - 3].rstrip() + '...'

def section(text: str, marker: str, stop_markers: list[str]) -> str:
    start = text.find(marker)
    if start == -1:
        return ''
    start += len(marker)
    end = len(text)
    for stop in stop_markers:
        pos = text.find(stop, start)
        if pos != -1:
            end = min(end, pos)
    return text[start:end].strip()

def first_bullet(text: str) -> str:
    match = re.search(r'^-\s+(.+)$', text, flags=re.MULTILINE)
    return compact(match.group(1)) if match else compact(text)

def plain_excerpt(text: str, limit: int = 280) -> str:
    text = re.sub(r'```.*?```', ' code example omitted ', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return compact(text, limit)

def realistic_prompt(title: str, tags: list[str], incorrect: str) -> str:
    tag_text = ' '.join(tags).lower()
    wrong = plain_excerpt(incorrect)
    if 'trigger' in tag_text or 'scope' in tag_text:
        return 'Can you review this Terraform change for our S3 bucket and make sure object upload validation is correct? I am not asking about this skill domain.'
    if any(token in tag_text for token in ['spring', 'java', 'dto', 'bean-validation', 'openapi', 'mockmvc']):
        if 'validation' in tag_text or 'bean-validation' in tag_text:
            return f"I'm adding a Spring Boot endpoint and invalid request payloads should return structured 400 responses. Current implementation: {wrong} What should I change and how should I test it?"
        if 'dto' in tag_text or 'boundaries' in tag_text:
            return f'Can you review this Spring Boot controller before I open the PR? Current implementation: {wrong} How should I separate the request, response, and domain models?'
        if 'openapi' in tag_text:
            return f'I changed a Spring Boot response DTO and need to keep the OpenAPI contract accurate for generated clients. Current approach: {wrong} What should I update and verify?'
        return f"I'm preparing a Spring Boot API model change for review and want to catch validation or serialization issues first. Current approach: {wrong} What should I change and how should I verify it?"
    if any(token in tag_text for token in ['react-native', 'mobile', 'biometric', 'offline', 'navigation', 'permission']):
        if 'navigation' in tag_text:
            return f'I am adding a React Native authenticated route and deep link path. Current approach: {wrong} What should I change and how should I test it?'
        if 'offline' in tag_text or 'sync' in tag_text or 'queue' in tag_text:
            return f'This React Native screen needs offline edits that replay after reconnect. Current implementation: {wrong} How should I structure the queue and failure handling?'
        if 'biometric' in tag_text or 'permission' in tag_text:
            return f'I am adding a React Native device capability flow and need safe fallback behavior. Current implementation: {wrong} What should I change and verify on iOS and Android?'
        return f"I'm preparing a React Native mobile change for review and want to catch platform or device-flow issues first. Current approach: {wrong} What should I change and how should I verify it?"
    if 'storybook' in tag_text:
        return f'I added a new component story, but it only renders the default state. Current approach: {wrong} What should I add before this is ready for review?'
    if 'form' in tag_text or 'controlled' in tag_text:
        return f"I'm building a login form and the submit button should stay disabled until both fields are valid. Current approach: {wrong} How should I structure the form state?"
    if 'accessibility' in tag_text or 'a11y' in tag_text:
        return f'I added an icon-only action and need it to work for keyboard and screen-reader users. Current implementation: {wrong} What should I change?'
    if 'state' in tag_text:
        return f'This feature has state updates spread across multiple modules and is becoming hard to reason about. Current implementation: {wrong} How should I refactor it?'
    return f"I'm preparing an implementation change for review and want to fix a concrete issue before opening the PR. Current approach: {wrong} What should I change and how should I verify it?"

def run() -> int:
    cases = []
    for idx, path in enumerate(sorted(Path('rules').glob('*.md')), start=1):
        if path.name.startswith('_'):
            continue
        text = path.read_text(encoding='utf-8')
        fm = frontmatter(text)
        title = fm.get('title', path.stem)
        when = section(text, '## When To Apply', ['## Evidence And Validation', '## References'])
        incorrect = section(text, '**Incorrect:**', ['**Correct:**', '## When To Apply'])
        correct = section(text, '**Correct:**', ['## When To Apply', '## Evidence And Validation'])
        evidence = section(text, '## Evidence And Validation', ['## References'])
        tags = [item.strip() for item in str(fm.get('tags', '')).split(',') if item.strip()]
        cases.append({
            'id': f'RULE-{idx:03d}',
            'rule_filename': path.name,
            'prompt': realistic_prompt(str(title), tags, incorrect or when),
            'expected_behavior': compact(correct or evidence or f'Apply the rule: {title}'),
            'negative_behavior': compact(incorrect or f'Do not ignore the rule: {title}'),
            'tags': tags,
        })
    Path('test-cases.json').write_text(json.dumps(cases, indent=2) + '\n', encoding='utf-8')
    print('test-cases.json rebuilt')
    return 0

if __name__ == '__main__':
    raise SystemExit(run())