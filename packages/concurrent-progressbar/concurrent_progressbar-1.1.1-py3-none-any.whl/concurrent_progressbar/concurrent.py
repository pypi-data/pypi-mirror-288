from multiprocessing import Process, Queue
import threading as th
from threading import Thread
from tqdm import tqdm
import time
import os


class _Concurrency(object):
    def __init__(self, num_workers, target: list, args: list, task_desc: list = None, tasks_at_a_time: int=None):
        super(_Concurrency, self).__init__()
        self._max_workers = min([len(a) for a in args])
        self._num_workers = num_workers if num_workers <= self._max_workers else self._max_workers
        self._target = target
        self._ntask = len(self._target)
        self._args = args
        assert len(self._args) == self._ntask, f"args len: {len(self._args)}, target len: {len(self._target)}"
        self._tasks_at_a_time = min(tasks_at_a_time if tasks_at_a_time is not None else self._ntask, os.cpu_count()) 
        self._task_desc = task_desc
        self._colors = ['WHITE', 'MAGENTA', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'CYAN']*self._ntask
        self._prog_bar = [tqdm(total=len(self._args[i]), dynamic_ncols=True, colour=self._colors[i], position=i, desc=f'Task {i}' if self._task_desc is None else self._task_desc[i]) for i in range(self._ntask)]
        self._queue = Queue()
        self._condition = th.Condition()

    def __str__(self):
        return f'No. of workers: {self._num_workers}\nNo. of tasks: {self._ntask}'
    
    def _status_update(self) -> None:
        while True:
            process_n = self._queue.get()
            if process_n == -1:
                break
            self._prog_bar[process_n].update()
            
    def _wait_for_process(self, _wait_queue: list, condition) -> None:
        while True:
            if len(_wait_queue) > 0:
                if _wait_queue[-1] == -1:
                    _wait_queue.pop()
                    for process in _wait_queue:
                        process.join()
                    try:  
                        with condition:
                            condition.notify()
                    except: pass
                    break
                
                flag, counter = True, 0
                while flag:
                    for n, p in enumerate(_wait_queue):
                        if not p.is_alive():
                            counter = n
                            _wait_queue.remove(_wait_queue[counter])
                            break
                    
                    if len(_wait_queue) < self._tasks_at_a_time:
                        try:
                            with condition:
                                condition.notify()
                        except: pass
                        flag = False
            
    def _wait(self, _wait_queue, condition) -> None:
        while True:
            if len(_wait_queue) > 0:
                if -1 in _wait_queue:
                    _wait_queue.pop()
                    for p in _wait_queue:
                        p.join()
                    try:
                        with condition:
                            condition.notify()
                    except: pass
                    break
    
                process = _wait_queue.pop(0)
                process.join()
     
                if len(_wait_queue) < self._num_workers:
                    try:
                        with condition:
                            condition.notify()
                    except: pass    
    
    def _task(self, i) -> None:
        condition = th.Condition()
        _wait_queue = []
        wait_t = Thread(target=self._wait, args=(_wait_queue, condition))
        wait_t.start()

        for arg in self._args[i]:
            p = self._create(i)
            p._args = arg
            p.start()
            
            if p.is_alive():
                _wait_queue.append(p)
            
            self._queue.put(int(i))
            
            if len(_wait_queue) > os.cpu_count():
                with condition:
                    condition.wait()

            try:
                while len(_wait_queue) >= self._num_workers:
                    with condition:
                        condition.wait()
            except KeyboardInterrupt as k:
                os._exit(0)
            except Exception as e:
                pass

        _wait_queue.append(-1)
        with condition:
            condition.wait()
    
    def run(self) -> None:
        t = Thread(target=self._status_update)
        t.start()
        
        _wait_queue, condition = [], th.Condition()
        
        wait_thread = Thread(target=self._wait_for_process, args=(_wait_queue, condition))
        wait_thread.start()
        
        for i in range(self._ntask):
            p = Process(target=self._task, args=(i,))
            p.start()
            
            if p.is_alive():
                _wait_queue.append(p)
            
            if len(_wait_queue) >= self._tasks_at_a_time:
                with condition:
                    condition.wait()
                    
        _wait_queue.append(-1)
        with condition:
            condition.wait()
        self._queue.put(-1)
    

class Multiprocessing(_Concurrency):
    def __init__(self, num_workers, target: list, args: list, task_desc: list = None, tasks_at_a_time=None):
        """Spawn the target method in different processes.

        Args:
            num_workers (_type_): Number of processes generated and executed parallel.
            target (list): The method to be executed.
            args (list): arguments for the targets
            task_desc (list, optional): _description_. Give name to the tasks.
        """
        super(Multiprocessing, self).__init__(
            num_workers=num_workers, target=target, args=args, task_desc=task_desc, tasks_at_a_time=tasks_at_a_time
        )
        
    def _create(self, i):
        return Process(target=self._target[i])
    
    def _create_process_pool(self, i):
        self.__setattr__(f'pool_{i}', [Process(target=self._target[i]) for _ in range(self._num_workers)])
            

class Multithreading(_Concurrency):
    def __init__(self, num_workers, target: list, args: list, task_desc: list = None, tasks_at_a_time=None):
        """Spawn the target method in different processes.

        Args:
            num_workers (_type_): Number of threads generated and executed parallel.
            target (list): The method to be executed.
            args (list): arguments for the targets
            task_desc (list, optional): _description_. Give name to the tasks.
        """
        super(Multithreading, self).__init__(
            num_workers=num_workers,
            target=target,
            args=args,
            task_desc=task_desc,
            tasks_at_a_time=tasks_at_a_time
        )
        
    def _create(self, i):
        return Thread(target=self._target[i])
    
    def _create_process_pool(self, i):
        self.__setattr__(f'pool_{i}', [Thread(target=self._target[i]) for _ in range(self._num_workers)])