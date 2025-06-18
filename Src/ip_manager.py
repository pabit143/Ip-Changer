import subprocess
import random
import time
import platform
from typing import Optional, List, Dict
import netifaces
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

class IPManager:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.available_interfaces = self._get_network_interfaces()
        
    def _get_network_interfaces(self) -> List[str]:
        """Get all available network interfaces"""
        try:
            return netifaces.interfaces()
        except:
            return []
    
    def _execute_command(self, command: str) -> bool:
        """Execute a shell command"""
        try:
            subprocess.run(command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_current_ip(self, interface: str = None) -> Optional[str]:
        """Get current IP address"""
        if not interface:
            interface = self.available_interfaces[0] if self.available_interfaces else None
            
        if not interface:
            return None
            
        try:
            addrs = netifaces.ifaddresses(interface)
            return addrs[netifaces.AF_INET][0]['addr']
        except:
            return None
    
    def change_ip(self, interface: str = None) -> bool:
        """Change IP address"""
        if self.os_type == 'linux':
            return self._change_ip_linux(interface)
        elif self.os_type == 'windows':
            return self._change_ip_windows(interface)
        else:
            print(Fore.RED + "Unsupported operating system")
            return False
    
    def _change_ip_linux(self, interface: str) -> bool:
        """Linux specific IP change logic"""
        if not interface:
            interface = self.available_interfaces[0] if self.available_interfaces else None
            
        if not interface:
            print(Fore.RED + "No network interfaces found")
            return False
            
        # Generate a random IP in 192.168.1.x range
        new_ip = f"192.168.1.{random.randint(2, 254)}"
        
        commands = [
            f"sudo ifconfig {interface} down",
            f"sudo ifconfig {interface} {new_ip} netmask 255.255.255.0",
            f"sudo ifconfig {interface} up"
        ]
        
        for cmd in commands:
            if not self._execute_command(cmd):
                print(Fore.RED + f"Failed to execute: {cmd}")
                return False
                
        print(Fore.GREEN + f"IP changed to {new_ip} on interface {interface}")
        return True
    
    def _change_ip_windows(self, interface: str) -> bool:
        """Windows specific IP change logic"""
        if not interface:
            print(Fore.YELLOW + "Interface must be specified on Windows")
            return False
            
        # Generate a random IP in 192.168.1.x range
        new_ip = f"192.168.1.{random.randint(2, 254)}"
        
        commands = [
            f'netsh interface ip set address name="{interface}" static {new_ip} 255.255.255.0 192.168.1.1'
        ]
        
        for cmd in commands:
            if not self._execute_command(cmd):
                print(Fore.RED + f"Failed to execute: {cmd}")
                return False
                
        print(Fore.GREEN + f"IP changed to {new_ip} on interface {interface}")
        return True
    
    def get_interface_details(self) -> Dict[str, Dict]:
        """Get details of all interfaces"""
        details = {}
        for interface in self.available_interfaces:
            try:
                addrs = netifaces.ifaddresses(interface)
                details[interface] = {
                    'ip': addrs.get(netifaces.AF_INET, [{}])[0].get('addr', 'N/A'),
                    'netmask': addrs.get(netifaces.AF_INET, [{}])[0].get('netmask', 'N/A'),
                    'mac': addrs.get(netifaces.AF_LINK, [{}])[0].get('addr', 'N/A')
                }
            except:
                details[interface] = {'error': 'Unable to get details'}
        return details
