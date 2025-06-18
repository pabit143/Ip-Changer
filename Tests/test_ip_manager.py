import unittest
from unittest.mock import patch, MagicMock
from ip_manager import IPManager
import netifaces
import platform

class TestIPManager(unittest.TestCase):
    def setUp(self):
        self.ip_manager = IPManager()
        
    @patch('netifaces.interfaces')
    def test_get_network_interfaces(self, mock_interfaces):
        # Test successful interface detection
        mock_interfaces.return_value = ['eth0', 'wlan0']
        interfaces = self.ip_manager._get_network_interfaces()
        self.assertEqual(interfaces, ['eth0', 'wlan0'])
        
        # Test error handling
        mock_interfaces.side_effect = Exception("Error")
        interfaces = self.ip_manager._get_network_interfaces()
        self.assertEqual(interfaces, [])

    @patch('subprocess.run')
    def test_execute_command(self, mock_run):
        # Test successful command execution
        mock_run.return_value = MagicMock(returncode=0)
        result = self.ip_manager._execute_command("test command")
        self.assertTrue(result)
        
        # Test failed command execution
        mock_run.side_effect = Exception("Error")
        result = self.ip_manager._execute_command("bad command")
        self.assertFalse(result)

    @patch('platform.system')
    def test_os_detection(self, mock_system):
        # Test Linux detection
        mock_system.return_value = 'Linux'
        ip_manager = IPManager()
        self.assertEqual(ip_manager.os_type, 'linux')
        
        # Test Windows detection
        mock_system.return_value = 'Windows'
        ip_manager = IPManager()
        self.assertEqual(ip_manager.os_type, 'windows')

    @patch('netifaces.ifaddresses')
    def test_get_current_ip(self, mock_ifaddresses):
        # Test successful IP retrieval
        mock_ifaddresses.return_value = {
            netifaces.AF_INET: [{'addr': '192.168.1.10', 'netmask': '255.255.255.0'}]
        }
        ip = self.ip_manager.get_current_ip('eth0')
        self.assertEqual(ip, '192.168.1.10')
        
        # Test no IP address case
        mock_ifaddresses.return_value = {}
        ip = self.ip_manager.get_current_ip('eth0')
        self.assertIsNone(ip)
        
        # Test interface error
        mock_ifaddresses.side_effect = Exception("Error")
        ip = self.ip_manager.get_current_ip('eth0')
        self.assertIsNone(ip)

    @patch('ip_manager.IPManager._change_ip_linux')
    @patch('ip_manager.IPManager._change_ip_windows')
    def test_change_ip(self, mock_win, mock_linux):
        # Test Linux IP change
        self.ip_manager.os_type = 'linux'
        mock_linux.return_value = True
        result = self.ip_manager.change_ip('eth0')
        self.assertTrue(result)
        mock_linux.assert_called_once_with('eth0')
        
        # Test Windows IP change
        self.ip_manager.os_type = 'windows'
        mock_win.return_value = True
        result = self.ip_manager.change_ip('Ethernet')
        self.assertTrue(result)
        mock_win.assert_called_once_with('Ethernet')
        
        # Test unsupported OS
        self.ip_manager.os_type = 'macos'
        result = self.ip_manager.change_ip('en0')
        self.assertFalse(result)

    @patch('ip_manager.IPManager._execute_command')
    def test_change_ip_linux(self, mock_execute):
        # Test successful Linux IP change
        mock_execute.side_effect = [True, True, True]
        result = self.ip_manager._change_ip_linux('eth0')
        self.assertTrue(result)
        self.assertEqual(mock_execute.call_count, 3)
        
        # Test failed Linux IP change
        mock_execute.side_effect = [True, False, True]
        result = self.ip_manager._change_ip_linux('eth0')
        self.assertFalse(result)

    @patch('ip_manager.IPManager._execute_command')
    def test_change_ip_windows(self, mock_execute):
        # Test successful Windows IP change
        mock_execute.return_value = True
        result = self.ip_manager._change_ip_windows('Ethernet')
        self.assertTrue(result)
        mock_execute.assert_called_once()
        
        # Test failed Windows IP change
        mock_execute.return_value = False
        result = self.ip_manager._change_ip_windows('Ethernet')
        self.assertFalse(result)

    @patch('netifaces.ifaddresses')
    def test_get_interface_details(self, mock_ifaddresses):
        # Test successful details retrieval
        mock_ifaddresses.return_value = {
            netifaces.AF_INET: [{'addr': '192.168.1.10', 'netmask': '255.255.255.0'}],
            netifaces.AF_LINK: [{'addr': '00:11:22:33:44:55'}]
        }
        details = self.ip_manager.get_interface_details()
        self.assertEqual(details['eth0']['ip'], '192.168.1.10')
        self.assertEqual(details['eth0']['netmask'], '255.255.255.0')
        self.assertEqual(details['eth0']['mac'], '00:11:22:33:44:55')
        
        # Test error case
        mock_ifaddresses.side_effect = Exception("Error")
        details = self.ip_manager.get_interface_details()
        self.assertEqual(details['eth0']['error'], 'Unable to get details')

    @patch('netifaces.interfaces')
    def test_no_interfaces(self, mock_interfaces):
        # Test behavior when no interfaces are available
        mock_interfaces.return_value = []
        ip_manager = IPManager()
        
        # Test methods that depend on interfaces
        self.assertEqual(ip_manager.get_current_ip(), None)
        self.assertEqual(ip_manager.get_interface_details(), {})
        self.assertFalse(ip_manager._change_ip_linux(None))

if __name__ == '__main__':
    unittest.main()
