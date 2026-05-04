import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base

EXPECTED_TABLES = {
    "member",
    "weight",
    "income",
    "income_category",
    "income_income_category",
    "expend",
    "expend_category",
    "expend_expend_category",
    "exercise_plan",
    "exercise_set",
    "exercise_category",
    "exercise_detail_category",
    "exercise_exercise_category",
}


def test_all_domain_models_registered() -> None:
    assert set(Base.metadata.tables.keys()) == EXPECTED_TABLES


def test_member_table_columns() -> None:
    member = Base.metadata.tables["member"]
    assert {c.name for c in member.columns} == {
        "member_id",
        "nickname",
        "email",
        "password",
        "created_at",
        "updated_at",
        "deleted_at",
    }
    assert member.c.email.unique is True


def test_owned_by_member_tables_have_member_fk() -> None:
    owned_tables = [
        "weight",
        "income",
        "income_category",
        "expend",
        "expend_category",
        "exercise_plan",
    ]
    for name in owned_tables:
        table = Base.metadata.tables[name]
        assert "member_id" in table.c, f"{name} missing member_id"
        fks = list(table.c.member_id.foreign_keys)
        assert len(fks) == 1
        assert fks[0].column.table.name == "member"


def test_exercise_set_fk_resolves_to_exercise_plan() -> None:
    table = Base.metadata.tables["exercise_set"]
    fks = list(table.c.exercise_id.foreign_keys)
    assert len(fks) == 1
    assert fks[0].column.table.name == "exercise_plan"


def test_system_wide_categories_have_no_member_id() -> None:
    for name in ("exercise_category", "exercise_detail_category"):
        table = Base.metadata.tables[name]
        assert "member_id" not in table.c, f"{name} should be system-wide"


@pytest.mark.asyncio
async def test_metadata_creates_on_sqlite() -> None:
    """SQLite 인메모리에 전체 스키마를 생성하고 세션이 열리는지 확인."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with session_factory() as session:
            assert session.bind is not None
    finally:
        await engine.dispose()
