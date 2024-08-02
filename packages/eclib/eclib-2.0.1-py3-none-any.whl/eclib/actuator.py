#! /usr/bin/env python3

from typing import Optional

import numpy as np
from multimethod import multidispatch
from numpy.typing import ArrayLike, NDArray

from eclib import dyn_elgamal, elgamal, gsw, gsw_lwe, paillier, regev
from eclib.system import Plant


class Actuator:
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
        sk: Optional[
            elgamal.SecretKey
            | dyn_elgamal.SecretKey
            | paillier.SecretKey
            | regev.SecretKey
            | gsw.SecretKey
            | gsw_lwe.SecretKey
        ] = None,
        delta: Optional[float] = None,
    ):
        self.cryptosystem = cryptosystem
        self.params = params
        self.sk = sk
        self.delta = delta

    def set_input(self, plant: Plant, controller_output: ArrayLike) -> None:
        u = np.asarray(controller_output, dtype=np.float64)

        match u.ndim:
            case 0 if plant.B.shape[1] == 1:
                plant.u = u.reshape(1)

            case 1 if plant.B.shape[1] == u.shape[0]:
                plant.u = u

            case 2 if plant.B.shape[1] == u.shape[0]:
                plant.u = u.reshape(-1)

            case _:
                raise ValueError

    def set_enc_input(
        self, plant: Plant, controller_output: NDArray[np.object_]
    ) -> None:
        match self.cryptosystem:
            case "elgamal" if (
                isinstance(self.params, elgamal.PublicParameters)
                and isinstance(self.sk, elgamal.SecretKey)
                and isinstance(self.delta, float)
            ):
                u = elgamal.dec_add(self.params, self.sk, controller_output, self.delta)

            case "dyn_elgamal" if (
                isinstance(self.params, dyn_elgamal.PublicParameters)
                and isinstance(self.sk, dyn_elgamal.SecretKey)
                and isinstance(self.delta, float)
            ):
                u = dyn_elgamal.dec_add(
                    self.params, self.sk, controller_output, self.delta
                )

            case "paillier" if (
                isinstance(self.params, paillier.PublicParameters)
                and isinstance(self.sk, paillier.SecretKey)
                and isinstance(self.delta, float)
            ):
                u = paillier.dec(self.params, self.sk, controller_output, self.delta)

            case "regev" if (
                isinstance(self.params, regev.PublicParameters)
                and isinstance(self.sk, regev.SecretKey)
                and isinstance(self.delta, float)
            ):
                u = regev.dec(self.params, self.sk, controller_output, self.delta)

            case "gsw" if (
                isinstance(self.params, gsw.PublicParameters)
                and isinstance(self.sk, gsw.SecretKey)
                and isinstance(self.delta, float)
            ):
                u = gsw.dec(self.params, self.sk, controller_output, self.delta)

            case "gsw_lwe" if (
                isinstance(self.params, gsw_lwe.PublicParameters)
                and isinstance(self.sk, gsw_lwe.SecretKey)
                and isinstance(self.delta, float)
            ):
                u = gsw_lwe.dec(self.params, self.sk, controller_output, self.delta)

            case _:
                raise NotImplementedError

        self.set_input(plant, u)
