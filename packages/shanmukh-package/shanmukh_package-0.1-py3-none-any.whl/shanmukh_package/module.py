
import sys

def check_dependencies():
    try:
        import pandas as pd
        print(f'pandas version: {pd.__version__}')
    except ImportError:
        print('pandas is not installed.')

    try:
        import matplotlib
        print(f'matplotlib version: {matplotlib.__version__}')
    except ImportError:
        print('matplotlib is not installed.')

    try:
        import numpy as np
        print(f'numpy version: {np.__version__}')
    except ImportError:
        print('numpy is not installed.')

    if sys.version_info >= (3, 9):
        print(f'Python version is {sys.version.split(" ")[0]}.This package requires Python < 3.10')
    else:
        print(f'Python version s {sys.version.split(" ")[0]}.')



if __name__ == "__main__":
    check_dependencies()
