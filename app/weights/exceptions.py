from app.shared.exceptions import NotFound


class WeightNotFound(NotFound):
    code = "WEIGHT_NOT_FOUND"
    message = "몸무게 기록을 찾을 수 없습니다."
