from heimdall.lib.pickles.logger import PicklesLogger
from heimdall.lib.singleton.singleton import SingletonMeta


class Pickles(metaclass=SingletonMeta):
    pickles_loads: int = None
    pickles_writes: int = None
    fn_hashes: dict = None
    logger: PicklesLogger = None

    def __init__(self, logger=None) -> None:
        self.pickles_loads = 0
        self.pickles_writes = 0
        self.fn_hashes = {}
        if logger:
            self.logger = logger
        else:
            self.logger = PicklesLogger()

    def cache(
        self,
        fn,
        *args,
        pickles_read_bypass=False,
        pickles_write_bypass=False,
        pickles_cache_path_prefix=None,
        **kwargs,
    ):
        import os
        import pickle

        if pickles_read_bypass and pickles_write_bypass:
            return fn(*args, **kwargs)

        if args is None:
            args = {}

        filename, relative_filename = self.pickle_filepath(
            fn, *args, **kwargs, pickles_cache_path_prefix=pickles_cache_path_prefix
        )
        file_exists = os.path.isfile(filename)
        if not pickles_read_bypass and file_exists:
            try:
                data = pickle.load(open(filename, "rb"))
                self.pickles_loads += 1
                self.logger.log(
                    "warning",
                    "PICKLES_LOAD",
                    loads=self.pickles_loads,
                    # function_path=self.function_path(fn),
                    filename=relative_filename,
                )
                return data
            except EOFError:
                pass

        data = fn(*args, **kwargs)
        # filename, relative_filename = self.pickle_filepath(fn, *args, **kwargs)

        if not pickles_write_bypass:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            pickle.dump(data, open(filename, "wb"))
            reason = "FILE_NOT_FOUND" if not file_exists else "WRITE_BYPASS_OFF"
            self.pickles_writes += 1
            self.logger.log(
                "warning",
                f"PICKLES_WRITE {reason}",
                writes=self.pickles_writes,
                # function_path=self.function_path(fn),
                filename=relative_filename,
            )

        return data

    @staticmethod
    def disassemble(fn):
        """Disassembla uma função e retorna a string"""
        import dis
        import re

        disassembled = dis.Bytecode(fn, first_line=False, current_offset=None).dis()
        disassembled = re.sub(r"0[xX][0-9a-fA-F]+", r"", disassembled)
        disassembled = re.sub(r" line [0-9]+", r"", disassembled)
        disassembled = re.split(r"[^\S\r\n]+", disassembled)
        disassembled[:] = [x for x in disassembled if x]
        disassembled = " ".join(disassembled[1:])
        return disassembled

    @staticmethod
    def digest(b):
        import hashlib

        return hashlib.sha256(b).hexdigest()

    def hash_fn(self, fn):
        """Retorna o hash do código de uma função"""
        if fn in self.fn_hashes:
            return self.fn_hashes[fn]
        disassembled = self.disassemble(fn)
        return self.digest(disassembled.encode())

    def gen_hashes(self, fn, *args, **kwargs):
        import pickle

        def hash_arg(v):
            if isinstance(v, list):
                return [hash_arg(i) for i in v]
            else:
                try:
                    return self.digest(pickle.dumps(v))
                except Exception:
                    return self.hash_fn(v)

        hashes = {
            "fn": self.hash_fn(fn) if fn else None,
            "args": [hash_arg(arg) for arg in args] if args else None,
            "kwargs": {k: hash_arg(v) for k, v in kwargs.items()} if kwargs else None,
        }
        return hashes

    def pickle_filepath(self, fn, *args, pickles_cache_path_prefix=None, **kwargs):
        import pickle

        from heimdall import PROJECT_FOLDER

        hash_str = self.digest(pickle.dumps(self.gen_hashes(fn, *args, **kwargs)))
        subfolder = self.function_path(fn)
        pickles_cache_path_prefix = (
            f"{pickles_cache_path_prefix}/" if pickles_cache_path_prefix else ""
        )
        fullpath = f"{PROJECT_FOLDER}/.pickles/{pickles_cache_path_prefix}{subfolder}/{hash_str}.pickle"
        relative_path = fullpath.replace(PROJECT_FOLDER, "")[1:]
        return fullpath, relative_path

    @staticmethod
    def function_path(fn):
        import inspect

        fullpath = inspect.getfile(fn)
        from heimdall import PROJECT_FOLDER

        relative_path = fullpath.replace(PROJECT_FOLDER, "")[1:].replace("/", ".")
        return f"{relative_path}:{fn.__qualname__}"
