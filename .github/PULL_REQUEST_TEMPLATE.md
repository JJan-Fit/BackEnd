<!--
PR 제목 컨벤션: <type>(<scope>): <설명>
type: feat | fix | refactor | docs | test | chore | perf | build | ci
예) feat(exercises): 운동 기록 생성 엔드포인트 추가
-->

## 변경 종류

<!-- 해당하는 항목에 [x] -->

- [ ] feat — 새 기능
- [ ] fix — 버그 수정
- [ ] refactor — 동작 동일, 구조만 변경
- [ ] docs — 문서
- [ ] test — 테스트만 추가/수정
- [ ] chore / build / ci — 설정·툴체인
- [ ] perf — 성능

## 요약

<!-- 무엇을 / 왜 바꿨는지. "어떻게" 는 코드가 말하므로 생략. -->

##

## 관련 이슈

<!-- Closes #123 / Refs #456 -->

## 테스트

<!-- 어떻게 검증했는지. 자동 테스트가 있으면 여기에. 수동 확인이면 명령/요청을 적어주세요. -->

- [ ] `uv run pytest` 통과
- [ ] `uv run ruff check app tests` 통과
- [ ] `uv run ruff format --check app tests` 통과
- [ ] `uv run mypy app` 통과
- [ ] (선택) 수동 검증:

## 영향 범위 / 마이그레이션

<!-- 다른 도메인에 영향이 있는지, DB 스키마/환경변수 변경이 있는지. -->

- [ ] 신규 환경변수 → `.env.example` 갱신함
- [ ] DB 스키마 변경 → 마이그레이션 포함
- [ ] 외부 API 계약(스키마) 변경 → 문서/프론트 공유 완료
- [ ] 위 모두 해당 없음

## 스크린샷 / 응답 예시

<!-- 응답 JSON, OpenAPI 변경 캡처 등이 있으면 첨부. 없으면 삭제. -->

## 리뷰어가 봐줬으면 하는 곳

<!-- 특정 결정에 대한 의견을 받고 싶다면 여기 -->
