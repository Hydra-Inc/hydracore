from typing import Iterator, List


def filter_seq(iter: Iterator, filters: List) -> List:
    iter = list(iter)
    for filt in filters:
        iter = list(filt(iter))
    return iter


def filter_by_sub_fld(iter: Iterator, field: str, sub: str) -> Iterator:
    for x in iter:
        if isinstance(x, str):
            if not sub in x:
                continue
        else:
            if not sub in getattr(x, field):
                continue
        yield x


def filter_by_bool_fld(iter: Iterator, field: str, val: bool = True) -> Iterator:
    for x in iter:
        if not getattr(x, field) == val:
            continue
        yield x
