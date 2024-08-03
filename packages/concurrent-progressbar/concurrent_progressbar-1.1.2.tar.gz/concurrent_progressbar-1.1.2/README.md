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


### Added multi-color bars and now number of tasks which can run in parallel can be provided as an argument.

```
pool = Multiprocessing(
                    num_workers=os.cpu_count(), 
                    target=[target_1, target_2], 
                    args=[[(i,) for i in range(1000)], [(j,) for j in range(100)]],
                    task_desc=["my-task-1", "my-task-2"],
                    tasks_at_a_time=1
    )
 # tasks_at_a_time=1 will run one task, when this task completed 
 # then next task will be executed. It is independent from num_workers argument.

pool.run()

```