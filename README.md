# JJan Fit BackEnd

운동 / 수입 / 지출 / 몸무게 트래킹 백엔드. FastAPI + Python 3.12.

## Quick start

```bash
# uv 설치 (최초 1회)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치 + venv 자동 생성
uv sync

# 환경변수 복사
cp .env.example .env

# pre-commit 훅 설치
uv run pre-commit install

# 개발 서버
uv run uvicorn app.main:app --reload
```

확인:

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

## 자주 쓰는 명령

| 목적 | 명령 |
| --- | --- |
| 서버 실행 | `uv run uvicorn app.main:app --reload` |
| 테스트 | `uv run pytest` |
| Lint | `uv run ruff check --fix app tests` |
| Format | `uv run ruff format app tests` |
| 타입 검사 | `uv run mypy app` |
| 의존성 추가 | `uv add <pkg>` (dev 는 `--dev`) |

Claude Code 사용 시 `/run`, `/test`, `/lint`, `/format`, `/typecheck`, `/check` 슬래시 커맨드도 사용 가능.

## 디렉터리

```
app/         FastAPI 코드
tests/       pytest
.claude/     Claude Code 팀 설정 (settings.local.json 은 개인용/gitignore)
.github/     CI 워크플로
```

협업/컨벤션 상세는 [CLAUDE.md](./CLAUDE.md) 참고.

## 기능 (예정)

- 로그인 / 인증
- 운동 기록
- 수입 / 지출 기록
- 몸무게 기록
- 카테고리 (운동·지출·수입 등)
