#!/usr/bin/env python3
import queue
import threading
import sys
if sys.platform == "win32":
    import multiprocess as multiprocessing
    from multiprocess.managers import BaseManager
else:
    from multiprocessing.managers import BaseManager
    import multiprocessing

from queue import LifoQueue
import time

class LifoManager(BaseManager):
    pass
LifoManager.register('LifoQueue', LifoQueue)


class Backtracker():
    """Allow for interaction with backtracking progress.
    Also handle threads."""

    def __init__(self, next_choice_func, *, starting_guesses=None, partial_checker=None, candidate_matcher=None, greedy=True):
        self.next_choice_func = next_choice_func
        self.starting_guesses = starting_guesses
        self.partial_checker = partial_checker
        self. candidate_matcher = candidate_matcher
        self.greedy = greedy
        self.manager = LifoManager()
        self.manager.start()
        # self.intermediate_queue = self.manager.LifoQueue()
        self.intermediate_queue = multiprocessing.Queue()
        self.solutions_queue = multiprocessing.Queue()
        self.mythreads = []

    def go(self, numthreads=1):
        for i in range(numthreads):
            self.mythreads.append(
                multiprocessing.Process(
                    target=thread_target_wrapper(
                        next_choice_func=self.next_choice_func,
                        starting_guesses=self.starting_guesses,
                        partial_checker=self.partial_checker,
                        candidate_matcher=self.candidate_matcher,
                        greedy=self.greedy,
                        intermediate_queue=self.intermediate_queue,
                        solutions_queue=self.solutions_queue
                    )
                )
            )
        for t in self.mythreads:
            time.sleep(0.1)
            t.start()

    def quit(self):
        pass



def thread_target_wrapper(*args, **kwargs):
    def wrapped():
        return backtrack(*args, **kwargs)
    return wrapped


def backtrack(next_choice_func, *, starting_guesses=None, partial_checker=None, candidate_matcher=None, greedy=True, intermediate_queue=None, solutions_queue=None):
    """next_choice_func should be a function that take a sequences and 
    returns any a list of all possible next items in that sequence.
    candidate_matcher should be a function that returns whether 
    Algorithm:
    Instantiate a queue.
    While it is not empty, pop all of its contents and put all the results
    of the next_choice_func back into the queue.
    Any results of the next_choice_func that match with the candidate_matcher 
    are put in a results queue.
    The algorithm has finished when the queue is empty.
    After that, the results queue is fed out.
    """
    if intermediate_queue is None:
        q = multiprocessing.Queue()
    else:
        q = intermediate_queue

    if solutions_queue is None:
        solutions = multiprocessing.Queue()
    else:
        solutions = solutions_queue
    assert not candidate_matcher is None, "A function to match final solutions must be provided."
    if starting_guesses:
        assert isinstance(starting_guesses[0], list), "Requires 2d list"
        assert isinstance(starting_guesses, list), "Requires 2d list"
        for i in starting_guesses:
            q.put(i)

    while q.qsize() > 0:
        try:
            partial = q.get()
            # print("partial",partial)
            for guess in next_choice_func(partial):
                head = tuple(partial) + tuple([guess])
                if candidate_matcher(head):
                    print(head)
                    solutions.put(head)
                    if greedy:
                        return [head]
                elif partial_checker(head):
                    q.put(head)

                else:
                    pass
                # print(head)
        except KeyboardInterrupt:
            return
    results = []
    for i in range(solutions.qsize()):
        results.append(solutions.get())
    return results
