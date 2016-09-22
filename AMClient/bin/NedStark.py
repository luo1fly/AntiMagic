import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from core import HouseStark


if __name__ == '__main__':

    HouseStark.ArgvHandler(sys.argv)