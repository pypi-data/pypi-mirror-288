import re
from typing import TypeAlias

from . import _pb


def to_KVValue(value: str, index: int | None = None) -> _pb.KVValue:
    return _pb.KVValue(Value=value, Index=index)


def from_KVValue(value: _pb.KVValue) -> str:
    return value.Value


KVDict: TypeAlias = dict[str, list[str]]


def to_KVData(kvd: KVDict) -> list[_pb.KVData]:
    out = []
    for key, val in kvd.items():
        vals = [to_KVValue(value=v, index=i) for i, v in enumerate(val)]
        out.append(_pb.KVData(Key=key, Values=vals))
    return out


def from_KVData(value: list[_pb.KVData]) -> KVDict:
    return {kv.Key: [from_KVValue(v) for v in kv.Values] for kv in list(value)}


_kv_idx = re.compile(r"{(\d+)}$")


def parse_KVDict(raw: list[str]) -> KVDict:
    """
    Convert a list of ``key:value``-format strings into a ``KVDict``.
    If ``key`` is of the format ``key{n}``, it is inserted at index ``n``.
    This is for converting KV1 values to a more reasonable format.

    :param raw: the raw key/value data
    :return: the parsed KV data
    """
    out: KVDict = {}

    for kv in raw:
        k, _, v = kv.partition(":")

        idx = -1
        if (match := _kv_idx.search(k)) is not None:
            idx = int(match.group(1))
            k = _kv_idx.sub(repl="", string=k, count=1)

        if k in out.keys():
            out[k].insert(idx, v)
        else:
            out[k] = [v]

    return out
