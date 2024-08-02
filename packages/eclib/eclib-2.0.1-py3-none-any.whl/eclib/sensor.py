#! /usr/bin/env python3

from typing import Optional

import numpy as np
from numpy.typing import ArrayLike, NDArray

from eclib import dyn_elgamal, elgamal, gsw, gsw_lwe, paillier, regev
from eclib.system import Plant


class Sensor:
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

    def get_output(self, plant: Plant) -> ArrayLike:
        plant.y = plant.C @ plant.x + plant.D @ plant.u

        if plant.y.shape[0] == 1:
            return plant.y.item()

        else:
            return plant.y

    def get_enc_output(self, plant: Plant) -> int | NDArray[np.object_]:
        plant.y = plant.C @ plant.x + plant.D @ plant.u

        match self.cryptosystem:
            case "elgamal" if (
                isinstance(self.params, elgamal.PublicParameters)
                and isinstance(self.pk, elgamal.PublicKey)
                and isinstance(self.delta, float)
            ):
                return elgamal.enc(self.params, self.pk, plant.y, self.delta)

            case "dyn_elgamal" if (
                isinstance(self.params, dyn_elgamal.PublicParameters)
                and isinstance(self.pk, dyn_elgamal.PublicKey)
                and isinstance(self.delta, float)
            ):
                return dyn_elgamal.enc(self.params, self.pk, plant.y, self.delta)

            case "paillier" if (
                isinstance(self.params, paillier.PublicParameters)
                and isinstance(self.pk, paillier.PublicKey)
                and isinstance(self.delta, float)
            ):
                return paillier.enc(self.params, self.pk, plant.y, self.delta)

            case "regev" if (
                isinstance(self.params, regev.PublicParameters)
                and isinstance(self.pk, regev.PublicKey)
                and isinstance(self.delta, float)
            ):
                return regev.enc(self.params, self.pk, plant.y, self.delta)

            case "gsw" if (
                isinstance(self.params, gsw.PublicParameters)
                and isinstance(self.pk, gsw.PublicKey)
                and isinstance(self.delta, float)
            ):
                return gsw.enc(self.params, self.pk, plant.y, self.delta)

            case "gsw_lwe" if (
                isinstance(self.params, gsw_lwe.PublicParameters)
                and isinstance(self.pk, gsw_lwe.PublicKey)
                and isinstance(self.delta, float)
            ):
                return gsw_lwe.enc(self.params, self.pk, plant.y, self.delta)

            case _:
                raise NotImplementedError
