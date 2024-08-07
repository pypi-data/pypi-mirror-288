# ulda

<!-- [![Build Status](https://github.com/Moran79/ulda/workflows/test/badge.svg?branch=master&event=push)](https://github.com/Moran79/ulda/actions?query=workflow%3Atest) -->

<!-- [![codecov](https://codecov.io/gh/Moran79/ulda/branch/master/graph/badge.svg)](https://codecov.io/gh/Moran79/ulda) -->
[![Python Version](https://img.shields.io/pypi/pyversions/ulda.svg)](https://pypi.org/project/ulda/)

Uncorrelated Linear Discriminant Analysis (ULDA), modified based on Ye, J., & Yu, B. (2005).

## Features

- Provide a more robust LDA module compared to one in `sklearn`, especially when handling perfect separation in high-dimensional data.
- Faster performance.

## Installation

```bash
pip install ulda
```

## Example

```python
import numpy as np
from ulda import ULDA
X = np.array([[0, 0], [0,1], [1, 1], [1, 2], [2, 2], [2, 3]])
y = np.array(['A', 'A', 'B', 'B', 'C', 'C'])
lda = ULDA()
lda.fit(X, y)
print(lda.predict([[1, 3]]))
```
