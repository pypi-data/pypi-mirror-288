
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import os

import pytest
from _pytest.mark import Expression,MarkMatcher
from _pytest.fixtures import FixtureRequest
from _pytest.runner import SetupState, call_and_report, show_test_item
import _pytest

pytest_config = None
remaining_case = 0
def run_one_test_item(session,i,item):

    nextitem = session.items[i + 1] if i + 1 < len(session.items) else None
    item.config.hook.pytest_runtest_protocol(item=item, nextitem=nextitem)
    if session.shouldfail:
        raise session.Failed(session.shouldfail)
    if session.shouldstop:
        raise session.Interrupted(session.shouldstop)


def pytest_addoption(parser):
    group = parser.getgroup('enable_multithreading')
    group.addoption("--th", action="store",default=0,
                    help="启用多线程运行")


def pytest_configure(config):
    global pytest_config
    pytest_config = config
    pytest_config.addinivalue_line("markers","notconcurrent")

from _pytest.nodes import Item
from typing import Optional
from typing import List
from _pytest.reports import TestReport
import time



def pytest_runtestloop(session: "Session") -> bool:
    global remaining_case
    matchexpr = "notconcurrent"
    expression = Expression.compile(matchexpr)
    concurrent_case_list = []
    th = pytest_config.getoption('--th')
    remaining_case = len(session.items)
    if not th:
        return None
    if session.testsfailed and not session.config.option.continue_on_collection_errors:
        raise session.Interrupted(
            "%d error%s during collection"
            % (session.testsfailed, "s" if session.testsfailed != 1 else "")
        )

    if session.config.option.collectonly:
        return True
    for i, item in enumerate(session.items):
        if expression.evaluate(MarkMatcher.from_item(item)):
            run_one_test_item(session, i, item)
        else:
            concurrent_case_list.append((run_one_test_item, session, i, item))

    with ThreadPoolExecutor(max_workers=int(th)) as executor:
        for case in concurrent_case_list:
            executor.submit(*case)
    return True


function_thread_lock_dict = defaultdict(threading.Lock)
def _fillfixtures(self) -> None:
    item = self._pyfuncitem
    fixturenames = getattr(item, "fixturenames", self.fixturenames)
    for argname in fixturenames:
        if argname not in item.funcargs:
            function_thread_lock = function_thread_lock_dict[argname]
            with function_thread_lock:
                item.funcargs[argname] = self.getfixturevalue(argname)


lock = threading.Lock()

def runtestprotocol(
    item: Item, log: bool = True, nextitem: Optional[Item] = None
) -> List[TestReport]:
    hasrequest = hasattr(item, "_request")
    if hasrequest and not item._request:  # type: ignore[attr-defined]
        item._initrequest()  # type: ignore[attr-defined]
    rep = call_and_report(item, "setup", log)
    reports = [rep]
    if rep.passed:
        if item.config.getoption("setupshow", False):
            show_test_item(item)
        if not item.config.getoption("setuponly", False):
            reports.append(call_and_report(item, "call", log))

    with lock:
        global remaining_case
        remaining_case = remaining_case - 1

    if nextitem != None:
        reports.append(call_and_report(item, "teardown", log, nextitem=nextitem))
    else:
        while remaining_case != 0:
            time.sleep(2)
        reports.append(call_and_report(item, "teardown", log, nextitem=nextitem))

    # after all teardown hooks have been called
    # want funcargs and request info to go away
    if hasrequest:
        item._request = False  # type: ignore[attr-defined]
        item.funcargs = None  # type: ignore[attr-defined]
    return reports


class ThreadLocalSetupState(threading.local, SetupState):
    def __init__(self):
        super(ThreadLocalSetupState, self).__init__()


class ThreadLocalEnviron(os._Environ):
    def __init__(self, env):
        super().__init__(
            env._data,
            env.encodekey,
            env.decodekey,
            env.encodevalue,
            env.decodevalue,
            env.putenv,
            env.unsetenv
        )
        if hasattr(env, 'thread_store'):
            self.thread_store = env.thread_store
        else:
            self.thread_store = threading.local()

    def __getitem__(self, key):
        if key == 'PYTEST_CURRENT_TEST':
            if hasattr(self.thread_store, key):
                value = getattr(self.thread_store, key)
                return self.decodevalue(value)
            else:
                raise KeyError(key) from None
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key == 'PYTEST_CURRENT_TEST':
            value = self.encodevalue(value)
            self.putenv(self.encodekey(key), value)
            setattr(self.thread_store, key, value)
        else:
            super().__setitem__(key, value)

    def __delitem__(self, key):
        if key == 'PYTEST_CURRENT_TEST':
            self.unsetenv(self.encodekey(key))
            if hasattr(self.thread_store, key):
                delattr(self.thread_store, key)
            else:
                raise KeyError(key) from None
        else:
            super().__delitem__(key)

    def __iter__(self):
        if hasattr(self.thread_store, 'PYTEST_CURRENT_TEST'):
            yield 'PYTEST_CURRENT_TEST'
        keys = list(self._data)
        for key in keys:
            yield self.decodekey(key)

    def __len__(self):
        return len(self.thread_store.__dict__) + len(self._data)

    def copy(self):
        return type(self)(self)


@pytest.mark.tryfirst
def pytest_sessionstart(session: "Session") -> None:
    _pytest.runner.SetupState = ThreadLocalSetupState

    os.environ = ThreadLocalEnviron(os.environ)

    FixtureRequest._fillfixtures = _fillfixtures
    _pytest.runner.runtestprotocol = runtestprotocol

