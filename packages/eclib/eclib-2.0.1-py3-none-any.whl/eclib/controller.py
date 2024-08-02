#! /usr/bin/env python3

from typing import Optional

import numpy as np
from numpy.typing import ArrayLike, NDArray

from eclib import dyn_elgamal, elgamal, gsw, gsw_lwe, paillier, regev


class Controller:
    def __init__(
        self,
        cryptosystem: Optional[str] = None,
        params: Optional[
            elgamal.PublicParameters
            | dyn_elgamal.PublicParameters
            | paillier.PublicParameters
            | regev.PublicParameters
            | gsw.PublicParameters
            | gsw_lwe.PublicParameters
        ] = None,
        pk: Optional[
            elgamal.PublicKey
            | dyn_elgamal.PublicKey
            | paillier.PublicKey
            | regev.PublicKey
            | gsw.PublicKey
            | gsw_lwe.PublicKey
        ] = None,
        delta: Optional[float] = None,
    ):
        self.cryptosystem = cryptosystem
        self.params = params
        self.pk = pk
        self.delta = delta
