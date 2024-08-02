from typing import List, Tuple, Union

import numpy as np
from numpy.typing import ArrayLike

__all__ = ["Numeric", "Scalar", "ArrayLike"]

Numeric = Union[int, float]

Scalar = Union[int, float]

class NOT_SET_TYPE:
    pass

NOT_SET = NOT_SET_TYPE()