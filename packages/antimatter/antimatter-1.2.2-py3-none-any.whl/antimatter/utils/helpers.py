import base64
from functools import partial

from antimatter.session import EncapsulateResponse, Session


def _b64_enc(data: EncapsulateResponse):
    # Take the data.raw as bytes, base64 encode it so that it can be decoded later to bytes
    return base64.b64encode(data.raw).decode("utf-8")


def _b64_dec(data: str):
    # Decode the base64 string to bytes
    return base64.b64decode(data)


def _encapsulate(data, sess: Session, write_context="default"):
    capsule = sess.encapsulate(data, write_context=write_context)
    return _b64_enc(capsule)


def get_encapsulate_partial(sess: Session, write_context="default"):
    return partial(_encapsulate, sess=sess, write_context=write_context)


def _load_capsule(data, sess: Session, read_context="default"):
    return sess.load_capsule(data=_b64_dec(data), read_context=read_context).data()


def get_load_capsule_partial(sess: Session, read_context="default"):
    return partial(_load_capsule, sess=sess, read_context=read_context)
