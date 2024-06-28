import unittest
from unittest.mock import patch, Mock

from ovos_utils.fakebus import FakeBus

_MOCK_CONFIG = {
    "admin": {
        "mock_admin_plugin": {},
        "mock_admin_enabled": {
            "enabled": True
        },
        "mock_admin_disabled": {
            "enabled": False
        }
    },
    "mock_enabled_plugin": {
        "enabled": True
    },
    "mock_disabled_plugin": {
        "enabled": False
    },
    "mock_plugin": {}
}


class MockPlugin:
    def __init__(self, *args, **kwargs):
        pass


class TestService(unittest.TestCase):
    def setUp(self):
        from ovos_PHAL.service import PHAL
        bus = FakeBus()
        self.service = PHAL(_MOCK_CONFIG, bus)

    @patch("ovos_PHAL.service.find_phal_plugins")
    def test_load_plugins(self, find_plugins):
        mock_plugins = {"mock_admin_plugin": Mock(),
                        "mock_admin_enabled": Mock(),
                        "mock_admin_disabled": Mock(),
                        "mock_disabled_plugin": Mock(),
                        "mock_plugin": MockPlugin,
                        "mock_enabled_plugin": Mock()}

        find_plugins.return_value = mock_plugins

        # Test without validators
        self.service.load_plugins()
        self.assertEqual(set(self.service.drivers.keys()),
                         {"mock_enabled_plugin"})
        self.service.drivers = {}

        # Tests with passing validators
        mock_plugins["mock_plugin"] = Mock()
        mock_plugins["mock_plugin"].validator.validate = Mock(return_value=True)
        mock_plugins["mock_enabled_plugin"].validator.validate = Mock(return_value=True)
        mock_plugins["mock_disabled_plugin"].validator.validate = Mock(return_value=True)
        self.service.load_plugins()
        self.assertEqual(set(self.service.drivers.keys()),
                         {"mock_plugin", "mock_enabled_plugin"})
        self.service.drivers = {}

        # Tests with failing validators
        mock_plugins["mock_plugin"].validator.validate.return_value = False
        mock_plugins["mock_enabled_plugin"].validator.validate.return_value = False
        mock_plugins["mock_disabled_plugin"].validator.validate.return_value = False
        self.service.load_plugins()
        self.assertEqual(self.service.drivers, {})
