"""
Pytest fixtures
"""
from xprocess import ProcessStarter
import pytest

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    # implementation_manager = ImplementationManager.get_instance()
    # implementation_manager.set_participant_service(ParticipantSeriviceLocal())
    # implementation_manager.initialize()


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """

@pytest.fixture
def myserver(xprocess):
    class Starter(ProcessStarter):
        # startup pattern
        pattern = "hello"

        # command to start process
        args = ['python3 ../../sail-aggregtor-fastapi/main_test.py']

    # ensure process is running and return its logfile
    logfile = xprocess.ensure("myserver", Starter)

    conn = # create a connection or url/port info to the server
    yield conn

    # clean up whole process tree afterwards
    xprocess.getinfo("myserver").terminate()


