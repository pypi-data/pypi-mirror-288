import uuid
import base62


def encode(u: uuid.UUID) -> str:
    return base62.encode(u.int)


def decode(s: str) -> str:
    return uuid.UUID(int=base62.decode(s))


def kuid1() -> str:
    return encode(uuid.uuid1())


def kuid3(namespace: uuid.UUID, name: str | bytes) -> str:
    return encode(uuid.uuid3(namespace, name))


def kuid4() -> str:
    return encode(uuid.uuid4())


def kuid5(namespace: uuid.UUID, name: str | bytes) -> str:
    return encode(uuid.uuid5(namespace, name))
