from heimdall.lib.pickles.logger import PicklesLogger
from heimdall.lib.pickles.pickles import Pickles


class SilentPicklesLogger(PicklesLogger):
    def log(self, log_type, *args, **kwargs):
        pass


pickles = Pickles(logger=SilentPicklesLogger())


def _fn_1(a, b, c=3):
    _ = sum([a for a in [1, 2, 3]])
    return a + b + c


fn_1 = _fn_1


def _fn_1(a, b, c=3):
    _ = sum([a for a in [1, 2, 3]])
    return a + b + c


fn_2 = _fn_1


class A:
    @staticmethod
    def fn_3(a, b, c=3):
        _ = sum([a for a in [1, 2, 3]])
        return a + b + c


def test_disassemble():
    disassembled_fn_1 = pickles.disassemble(fn_1)
    disassembled_fn_2 = pickles.disassemble(fn_2)
    disassembled_fn_3 = pickles.disassemble(A.fn_3)
    assert disassembled_fn_1 == disassembled_fn_2
    assert disassembled_fn_1 != disassembled_fn_3


def test_hash_fn():
    hash_fn_1 = pickles.hash_fn(fn_1)
    hash_fn_2 = pickles.hash_fn(fn_2)
    hash_fn_3 = pickles.hash_fn(A.fn_3)
    assert hash_fn_1 == hash_fn_2
    assert hash_fn_2 != hash_fn_3


def test_hash_args():
    a = {"a": 1, "b": 2}
    b = {"a": 1, "b": 2, "c": 3}
    del b["c"]
    assert pickles.gen_hashes(None, a) == pickles.gen_hashes(None, b)


def test_hash_fn_args():
    a = {"a": 1, "b": 2}
    b = {"a": 1, "b": 2, "c": 3}
    del b["c"]
    assert pickles.gen_hashes(fn_1, **a) == pickles.gen_hashes(fn_2, **b)


def test_pickles_result():
    import os

    def fn(a, b, c):
        return {"a": a + 1, "b": b + 1, "c": c + 1}

    kwargs = {"a": 1, "b": 2, "c": 3}
    actual = pickles.cache(fn, **kwargs)
    expected = {"a": 2, "b": 3, "c": 4}
    assert actual == expected

    file_path, _ = pickles.pickle_filepath(fn, **kwargs)
    assert os.path.isfile(file_path)

    os.remove(file_path)
    assert not os.path.isfile(file_path)


def test_pickles_cache():
    import os
    from time import sleep

    def fn():
        from datetime import datetime

        return datetime.now()

    past = pickles.cache(fn)
    sleep(0.0001)
    future = fn()
    cached = pickles.cache(fn)
    assert past < future
    assert past == cached

    file_path, _ = pickles.pickle_filepath(fn)
    assert os.path.isfile(file_path)

    os.remove(file_path)
    assert not os.path.isfile(file_path)


def test_disassemble_generator():
    def gen1():
        yield 1

    def gen2():
        yield 1

    def fn():
        def gen3():
            yield 1

        return gen3()

    def gen4():
        yield 2

    igen1 = gen1()
    igen2 = gen2()
    igen3 = fn()
    igen4 = gen4()

    disassembled_gen_1 = pickles.disassemble(igen1)
    disassembled_gen_2 = pickles.disassemble(igen2)
    disassembled_gen_3 = pickles.disassemble(igen3)
    disassembled_gen_4 = pickles.disassemble(igen4)
    assert disassembled_gen_1 == disassembled_gen_2 == disassembled_gen_3
    assert disassembled_gen_1 != disassembled_gen_4
