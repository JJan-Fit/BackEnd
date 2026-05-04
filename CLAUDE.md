# JJan Fit BackEnd

운동 / 수입 / 지출 / 몸무게를 카테고리화해 기록하는 트래커 백엔드. FastAPI 기반.

## 스택

Python 3.12 · FastAPI · Pydantic v2 · SQLAlchemy 2.x (async) · asyncmy · MySQL 8 · uv · Ruff · mypy(strict) · pytest

## 디렉터리

```
app/
├── main.py            # FastAPI 엔트리 (create_app + lifespan)
├── core/config.py     # pydantic-settings
├── db/                # DeclarativeBase, async engine/session, BigIntPK
├── shared/            # 응답 envelope, 도메인 예외, 핸들러, mixins
├── auth/              # 회원가입/로그인 (JWT, bcrypt)  ← 구현됨
├── weights/           # 몸무게 CRUD                     ← 구현됨
├── incomes/, expenses/, exercises/   # 모델만 존재. 라우터/서비스는 미구현
tests/                 # pytest (도메인별 디렉터리)
.github/               # 이슈/PR 템플릿, CI
pyproject.toml         # 의존성 + ruff/mypy/pytest 설정
uv.lock                # 의존성 락 (커밋 필수)
```

## 셋업

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
cp .env.example .env             # 본인 값으로 수정
uv run pre-commit install
uv run uvicorn app.main:app --reload
```

확인: `curl http://localhost:8000/health` → `{"status":"ok"}`

## DB

- 로컬 개발: MySQL 8 (`jjanfit` DB). `.env` 의 `DATABASE_URL=mysql+asyncmy://...`
- `DATABASE_AUTO_CREATE=true` 로 두면 기동 시 누락 테이블 자동 생성. 운영/스테이징은 반드시 `false`
- 테스트는 `aiosqlite` 인메모리 DB (실 MySQL 불필요). PK 는 `BigIntPK = BigInteger().with_variant(Integer, "sqlite")` 로 dialect 별 자동증가 호환

## API 응답 / 에러 컨벤션

모든 도메인 라우터는 동일 envelope:

```json
{ "success": true,  "data": {...},  "error": null }
{ "success": false, "data": null,   "error": {"code": "...", "message": "...", "detail": null} }
```

- 성공: `app.shared.response.ok(data)` helper
- 실패: `app.shared.exceptions` 의 도메인 예외 (`Conflict`, `NotFound`, `Unauthorized`, ...) 를 raise → 핸들러가 envelope 으로 변환
- 라우터에서 `HTTPException` 직접 사용 지양

## 인증

- `Authorization: Bearer <jwt>` 헤더
- `app.auth.deps.get_current_member` Depends 가 토큰 검증 + Member 주입
- 본인 소유 검증은 service 에서 `member_id` 일치 확인. 다른 사용자 리소스는 일관 404 (존재 누설 X)

## 개발 워크플로 — TDD 필수

새 기능 / 버그 수정은 항상:

1. 🔴 **Red** — 실패하는 테스트부터 작성 → `uv run pytest -x` 로 빨강 확인
2. 🟢 **Green** — 최소 구현으로 통과
3. ♻️ **Refactor** — 초록 유지하며 구조 정리

버그 수정도 회귀 테스트 먼저 → 수정 → 통과.

## 자주 쓰는 명령

| 목적 | 명령 |
| --- | --- |
| 서버 실행 | `uv run uvicorn app.main:app --reload` |
| 테스트 | `uv run pytest` |
| Lint | `uv run ruff check --fix app tests` |
| Format | `uv run ruff format app tests` |
| 타입 검사 | `uv run mypy app` |
| 전체 검증 | 위 4개 순차 실행 (CI 와 동일) |

## 코드 컨벤션

- **타입 힌트 필수** (mypy strict). `Optional[T]` 대신 `T | None`, `list[int]` 등 PEP 585.
- **Pydantic v2** 문법: `BaseModel` + `model_config`, `Field(...)`. v1 의 `class Config:` 금지
- I/O 핸들러/서비스는 `async def`. 순수 계산은 sync.
- 환경 의존 값은 `app.core.config.settings` 만. `os.environ` 직접 호출 금지
- 도메인 모듈 구조: `router.py` / `schemas.py` / `service.py` / `repository.py` / `models.py` / `exceptions.py`

## 협업 규칙

- 브랜치: `main` 은 항상 배포 가능. 작업은 `feat/<scope>`, `fix/<scope>`, `refactor/<scope>` 로
- 커밋/PR 제목: gitmoji + Conventional — 예) `✨ feat(weights): 몸무게 CRUD`
- PR 전 lint + format + typecheck + test 모두 통과. CI 가 동일 검증 강제
- 새 환경변수 → `.env.example` 같은 PR 에서 갱신
- 시크릿 / `.env` / `*.pem` 커밋 금지 (gitignore 처리됨)
