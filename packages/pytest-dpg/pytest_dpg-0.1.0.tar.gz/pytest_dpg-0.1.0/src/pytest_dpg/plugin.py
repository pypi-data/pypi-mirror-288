import multiprocess as mp
import pyautogui
import pytest

from pytest_dpg.invoker import TestInvoker

# External multiprocess is used for greater
# chance of serialization without errors
mp.set_start_method("spawn")

pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0


@pytest.fixture
def dpgtester():
    tester = TestInvoker()
    yield tester
    tester.stop_gui()
