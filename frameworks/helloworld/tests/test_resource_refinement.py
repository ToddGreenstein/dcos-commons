import pytest
import sdk_install
import sdk_utils
from tests import config


pytestmark = pytest.mark.skipif(
    sdk_utils.is_strict_mode() and sdk_utils.dcos_version_less_than('1.11'),
    reason="secure hierarchical roles are only supported on 1.11+")

@pytest.fixture(scope='module', autouse=True)
def configure_package(configure_security):
    try:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)
        options = {
            "service": {
                "yaml": "pre-reserved"
            }
        }

        sdk_install.install(config.PACKAGE_NAME,
                            config.SERVICE_NAME,
                            config.DEFAULT_TASK_COUNT,
                            additional_options=options)

        yield  # let the test session execute
    finally:
        sdk_install.uninstall(config.PACKAGE_NAME, config.SERVICE_NAME)


@pytest.mark.sanity
@pytest.mark.smoke
@pytest.mark.dcos_min_version('1.10')
def test_install():
    config.check_running(config.SERVICE_NAME)
