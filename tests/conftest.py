"""테스트는 DB 없이 돌도록 보장한다.

OS 환경변수가 ``.env`` 보다 우선이므로, ``Settings()`` 가 처음 인스턴스화되기
전에 ``DATABASE_AUTO_CREATE=false`` 로 강제한다. pytest 가 conftest.py 를
다른 테스트 모듈보다 먼저 로드하기 때문에 안전하다.
"""

import os

os.environ["DATABASE_AUTO_CREATE"] = "false"
