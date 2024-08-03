from base64 import b64encode
from hashlib import blake2b


TT_HASHED_ID_PREFIX = 'HID#'
TT_HASHED_ID_SIZE = 21


def generate_hashed_id(id_type: str, id_data: str) -> str:
    """Hashed ID generation routine."""
    return TT_HASHED_ID_PREFIX + b64encode(
        blake2b(
            ':'.join((id_type, id_data)).encode('utf-8'),
            digest_size=TT_HASHED_ID_SIZE).digest(),
        altchars=b'-_').decode('utf-8')
