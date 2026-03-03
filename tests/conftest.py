import json
import pytest
from pathlib import Path

from src.clients.albums_client import AlbumsClient
from src.core.logger import get_logger
from src.core.config_loader import load_config
from src.clients.users_client import UsersClient
from src.clients.posts_client import PostsClient
from src.clients.comments_client import CommentsClient


@pytest.fixture(scope="session")
def config():
    """
    Fixture de sesiune care încarcă config-ul global.
    """
    return load_config()


@pytest.fixture(scope="session")
def test_data():
    """
    Fixture care încarcă data/test_data.json.
    """
    project_root = Path(__file__).resolve().parents[1]  # needs this because it has to search for the file starting
    # from the project root
    with open(project_root / "data" / "test_data.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def users_client(config):
    return UsersClient(
        base_url=config["base_url"],
        timeout=config["timeout"],
    )


@pytest.fixture
def posts_client(config):
    return PostsClient(
        base_url=config["base_url"],
        timeout=config["timeout"]
    )


@pytest.fixture
def comments_client(config):
    return CommentsClient(
        base_url=config["base_url"],
        timeout=config["timeout"]
    )


@pytest.fixture
def albums_client(config):
    return AlbumsClient(
        base_url=config["base_url"],
        timeout=config["timeout"]
    )


# hooks for Start test/End test style in logs
logger = get_logger("pytest")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    logger.info(f"=== START {item.name} ===")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield
    logger.info(f"=== END {item.name} ===")
    logger.info(f"================================================================================")
# hooks for Start test/End test style in logs


# hook for setting a different timeout for each test
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # We care about the actual test call phase (not setup/teardown)
    if report.when != "call":
        return

    if report.failed:
        # pytest-timeout typically fails the test with a timeout message.
        # We detect it via the longrepr text.
        long_text = getattr(report, "longreprtext", "") or str(report.longrepr)
        if "Timeout" in long_text.lower():
            logger.error(f"TEST TIMEOUT: {item.nodeid}")
# hook fot setting a different timeout for each test


# setting the environments
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Target environment")
# setting the environments





