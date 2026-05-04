"""DB 진입점.

이 모듈을 import 하면 모든 도메인의 ORM 모델이 ``Base.metadata`` 에 등록된다.
Alembic / ``Base.metadata.create_all`` / 테스트 fixture 가 전체 스키마를 보려면
``from app.db import Base`` 가 필요하다.
"""

# 도메인 모델 등록 (import 부수효과로 metadata 채워짐)
from app.auth import models as _auth_models  # noqa: F401
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine, get_db
from app.exercises import models as _exercises_models  # noqa: F401
from app.expenses import models as _expenses_models  # noqa: F401
from app.incomes import models as _incomes_models  # noqa: F401
from app.weights import models as _weights_models  # noqa: F401

__all__ = ["AsyncSessionLocal", "Base", "engine", "get_db"]
