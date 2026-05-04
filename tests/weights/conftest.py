"""weights 도메인 테스트용 fixture.

- ``db_session`` : 인메모리 SQLite 에 전체 스키마 생성, AsyncSession 1개 yield
- ``client``     : ``get_db`` Depends 를 ``db_session`` 으로 대체
- ``signup_and_token`` : 헬퍼 함수 fixture — 가입 + 로그인 → bearer 토큰 / member_id
- ``auth_headers`` : 기본 사용자 토큰의 Authorization 헤더 dict
"""

from collections.abc import AsyncIterator, Callable

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base, get_db
from app.main import app


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[TestClient]:
    async def _override() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = _override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
def signup_and_token(client: TestClient) -> Callable[..., tuple[int, str]]:
    """Returns (member_id, access_token)."""

    def _factory(
        email: str = "user@example.com",
        password: str = "secret123",
        nickname: str = "user",
    ) -> tuple[int, str]:
        signup = client.post(
            "/auth/signup",
            json={"email": email, "password": password, "nickname": nickname},
        )
        assert signup.status_code == 201, signup.text
        member_id = int(signup.json()["data"]["member_id"])

        login = client.post("/auth/login", json={"email": email, "password": password})
        assert login.status_code == 200, login.text
        token = str(login.json()["data"]["access_token"])
        return member_id, token

    return _factory


@pytest_asyncio.fixture
def auth_headers(
    signup_and_token: Callable[..., tuple[int, str]],
) -> dict[str, str]:
    _, token = signup_and_token()
    return {"Authorization": f"Bearer {token}"}
