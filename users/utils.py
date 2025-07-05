import jwt
from django.conf import settings
from datetime import datetime, timedelta


def create_invite_token(user_id: int) -> str:
    """
    Генерирует JWT токен с user_id, срок действия — 2 дня.
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=2),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def decode_token(token: str) -> int:
    """
    Декодирует токен и возвращает user_id. Если токен недействителен — выбрасывает исключение.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise ValueError("Срок действия ссылки истёк")
    except jwt.InvalidTokenError:
        raise ValueError("Недопустимый токен")
