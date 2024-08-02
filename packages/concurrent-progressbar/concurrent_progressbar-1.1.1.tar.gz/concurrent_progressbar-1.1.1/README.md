# Multiple Progressbars

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This package is used to track the processes executed in the program. It will show individual progress bar for each task alloted using this package. It runs each task in separate process.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

pip install concurrent-progressbar

## Usage <a name = "usage"></a>
```
import os
from concurrent_progressbar.concurrent import Multithreading, MultiProcessing


def target_1(i):
    pass

def target_2(j):
    pass


pool = Multithreading(
                    num_workers=os.cpu_count(), 
                    target=[target_1, target_2], 
                    args=[[(i,) for i in range(1000)], [(j,) for j in range(100)]]
    )

pool.run()

# OR

pool = Multiprocessing(
                    num_workers=os.cpu_count(), 
                    target=[target_1, target_2], 
                    args=[[(i,) for i in range(1000)], [(j,) for j in range(100)]]
    )

pool.run()
```
