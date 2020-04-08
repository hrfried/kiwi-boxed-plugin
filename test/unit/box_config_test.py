import logging
from mock import patch
from pytest import (
    raises, fixture
)

from kiwi_boxed_plugin.box_config import BoxConfig
from kiwi_boxed_plugin.exceptions import KiwiBoxPluginConfigError


class TestBoxConfig:
    @fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

    @patch('kiwi_boxed_plugin.defaults.Defaults.get_box_config_file')
    def setup(self, mock_get_box_config_file):
        mock_get_box_config_file.return_value = '../data/boxes.yml'
        with self._caplog.at_level(logging.INFO):
            self.box_config = BoxConfig('suse')

    @patch('yaml.safe_load')
    @patch('kiwi_boxed_plugin.defaults.Defaults.get_box_config_file')
    def test_setup_raises(self, mock_get_box_config_file, mock_yaml_safe_load):
        mock_get_box_config_file.return_value = '../data/boxes.yml'
        mock_yaml_safe_load.side_effect = Exception
        with raises(KiwiBoxPluginConfigError):
            BoxConfig('suse')

    def test_get_box_memory_mbytes(self):
        assert self.box_config.get_box_memory_mbytes() == 4096

    def test_get_box_root(self):
        assert self.box_config.get_box_root() == '/dev/vda1'

    def test_get_box_console(self):
        assert self.box_config.get_box_console() == 'hvc0'

    def test_get_box_kernel_cmdline(self):
        assert self.box_config.get_box_kernel_cmdline() == 'rd.plymouth=0'

    def test_get_box_source(self):
        assert self.box_config.get_box_source() == \
            'obs://Virtualization:Appliances:SelfContained/images'

    def test_get_box_packages_file(self):
        assert self.box_config.get_box_packages_file() == \
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.packages'

    def test_get_box_files(self):
        assert self.box_config.get_box_files() == [
            'SUSE-Box.x86_64-1.42.1-Kernel-BuildBox.tar.xz',
            'SUSE-Box.x86_64-1.42.1-System-BuildBox.qcow2'
        ]
