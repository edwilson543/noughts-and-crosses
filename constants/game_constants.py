import time
from enum import Enum

class GameValue(Enum):
    """Enum for the different options to enter on the Noughts and Crosses board."""
    X = 1
    O = -1

import numpy as np

arr = np.array([[1, 2], [3, 4]])
print(arr.astype(str).tolist())
