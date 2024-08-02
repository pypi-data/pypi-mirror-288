#! /usr/bin/env python3

from typing import Optional

import numpy as np
from numpy.typing import ArrayLike


class Plant:
    def __init__(
        self,
        A: ArrayLike,
        B: ArrayLike,
        C: ArrayLike,
        D: ArrayLike,
        x0: Optional[ArrayLike] = None,
    ):
        A_ = np.asarray(A, dtype=np.float64)
        B_ = np.asarray(B, dtype=np.float64)
        C_ = np.asarray(C, dtype=np.float64)
        D_ = np.asarray(D, dtype=np.float64)
        x0_ = np.asarray(x0, dtype=np.float64)

        match A_.ndim:
            case 0:
                self.A = A_.reshape(1, 1)

            case 2 if A_.shape[0] == A_.shape[1]:
                self.A = A_

            case _:
                raise ValueError

        match B_.ndim:
            case 0 if self.A.shape[0] == 1:
                self.B = B_.reshape(1, 1)

            case 1 if self.A.shape[1] == 1:
                self.B = B_.reshape(1, len(B_))

            case 2 if self.A.shape[1] == B_.shape[0]:
                self.B = B_

            case _:
                raise ValueError

        match C_.ndim:
            case 0 if self.A.shape[0] == 1:
                self.C = C_.reshape(1, 1)

            case 1 if self.A.shape[1] == len(C_):
                self.C = C_.reshape(1, len(C_))

            case 2 if self.A.shape[1] == C_.shape[1]:
                self.C = C_

            case _:
                raise ValueError

        match D_.ndim:
            case 0 if self.B.shape[1] == 1 and self.C.shape[0] == 1:
                self.D = D_.reshape(1, 1)

            case 1 if self.B.shape[1] == len(D_) and self.C.shape[0] == 1:
                self.D = D_.reshape(1, len(D_))

            case 2 if (
                self.B.shape[1] == D_.shape[1] and self.C.shape[0] == D_.shape[0]
            ):
                self.D = D_

            case _:
                raise ValueError

        if x0 is None:
            self.x = np.zeros(self.A.shape[0], dtype=np.float64)

        else:
            match x0_.ndim:
                case 0 if self.A.shape[0] == 1:
                    self.x = x0_.reshape(1)

                case 1 if self.A.shape[1] == x0_.shape[0]:
                    self.x = x0_

                case 2 if (self.A.shape[1] == x0_.shape[0] and x0_.shape[1] == 1):
                    self.x = x0_.reshape(-1)

                case _:
                    raise ValueError

        self.u = np.zeros(self.B.shape[1], dtype=np.float64)
        self.y = np.zeros(self.C.shape[0], dtype=np.float64)

    def update(self) -> None:
        self.x = self.A @ self.x + self.B @ self.u

    def reset(
        self,
        x0: Optional[ArrayLike] = None,
        u: Optional[ArrayLike] = None,
        y: Optional[ArrayLike] = None,
    ) -> None:
        x0_ = np.asarray(x0)
        u_ = np.asarray(u)
        y_ = np.asarray(y)

        if x0 is None:
            self.x = np.zeros(self.A.shape[0], dtype=np.float64)

        else:
            match x0_.ndim:
                case 0 if self.A.shape[0] == 1:
                    self.x = x0_.reshape(1)

                case 1 if self.A.shape[1] == x0_.shape[0]:
                    self.x = x0_

                case 2 if (self.A.shape[1] == x0_.shape[0] and x0_.shape[1] == 1):
                    self.x = x0_.reshape(-1)

                case _:
                    raise ValueError

        if u is None:
            self.u = np.zeros(self.B.shape[1], dtype=np.float64)

        else:
            match u_.ndim:
                case 0 if self.B.shape[1] == 1:
                    self.u = u_.reshape(1)

                case 1 if self.B.shape[1] == u_.shape[0]:
                    self.u = u_

                case 2 if (self.B.shape[1] == u_.shape[0] and u_.shape[1] == 1):
                    self.u = u_.reshape(-1)

                case _:
                    raise ValueError

        if y is None:
            self.y = np.zeros(self.C.shape[1], dtype=np.float64)

        else:
            match y_.ndim:
                case 0 if self.C.shape[1] == 1:
                    self.y = y_.reshape(1)

                case 1 if self.C.shape[1] == y_.shape[0]:
                    self.y = y_

                case 2 if (self.C.shape[1] == y_.shape[0] and y_.shape[1] == 1):
                    self.y = y_.reshape(-1)

                case _:
                    raise ValueError
