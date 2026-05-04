"""DB 타입 별칭.

``BigIntPK`` 는 모든 도메인의 PK 에 사용한다. MySQL 은 ``BIGINT AUTO_INCREMENT``,
SQLite 는 ``INTEGER`` (rowid 별칭) 로 매핑돼 테스트 시 자동증가가 동작한다.
"""

from sqlalchemy import BigInteger, Integer

BigIntPK = BigInteger().with_variant(Integer(), "sqlite")
