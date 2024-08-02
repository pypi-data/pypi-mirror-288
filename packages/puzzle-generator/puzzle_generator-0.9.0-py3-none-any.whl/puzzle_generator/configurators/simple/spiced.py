import secrets
import typing

from ... import bytestr_utils as bu
from ...encryption_algorithms.simple import common
from ...encryption_algorithms.simple import spiced as sse
from ...puzzle_data_encryption import decrypt_data
from .. import common as cc
from .common import MODULES, scrypt_params, scrypt_params_to_code_str
from ...run_puzzle import run_puzzle
from ...bytes_utils import bytes_to_int, split


def _get_some_spices():
    return [secrets.token_bytes(3) for _ in range(20)]


def _list_of_bytes_to_str(in_list: typing.List[bytes]) -> str:
    return str([bu.bytes_to_bytestr(_) for _ in in_list])


def _list_of_bytes_to_codestr(in_list: typing.List[bytes]) -> str:
    raw: str = _list_of_bytes_to_str(in_list)
    return f"[bytestr_to_bytes(_) for _ in {raw}]"


class Spiced:
    def __init__(self, **kwargs):
        self._scrypt_params = scrypt_params(**kwargs)
        self._signature_hasher = kwargs.get("signature_hasher", cc.DefaultHasher)
        self._proc_spices = kwargs.get("proc_spices", _get_some_spices())
        self._signature_spices = kwargs.get("signature_spices", _get_some_spices())

    def get_modules(self) -> typing.List[str]:
        return MODULES

    def get_encrypt(self):
        return sse.get_encrypt(
            self._signature_hasher,
            self._proc_spices,
            self._signature_spices,
            self._scrypt_params,
        )

    def get_needed_objects(self):
        return [
            common.hash_bytes,
            common.derive_key,
            common.split_data_and_signature,
            common.xor_bytes,
            bu.bytestr_to_bytes,
            sse.get_decrypt,
            bytes_to_int,
            split,
            decrypt_data,
            run_puzzle,
        ]

    def get_constants_str(
        self,
    ) -> str:
        proc_spices: str = (
            f"_PROC_SPICES = {_list_of_bytes_to_codestr(self._proc_spices)}"
        )
        signature_spices: str = (
            f"_SIGNATURE_SPICES = {_list_of_bytes_to_codestr(self._signature_spices)}"
        )
        _scrypt_params = scrypt_params_to_code_str(**self._scrypt_params)
        decrypt: str = (
            "_DECRYPT = get_decrypt("
            f"{cc.get_hasher_name(self._signature_hasher)}, "
            "_PROC_SPICES, "
            "_SIGNATURE_SPICES, "
            "_SCRYPT_PARAMS)"
        )
        return "\n".join([proc_spices, signature_spices, _scrypt_params, decrypt])
