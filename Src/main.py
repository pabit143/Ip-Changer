import argparse
import time
from ip_manager import IPManager
from colorama import Fore, Style
from typing import Optional

def print_banner():
    """Print the custom ASCII banner"""
    banner = r"""
     ██╗██████╗        ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
     ██║██╔══██╗      ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
     ██║██████╔╝█████╗██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
     ██║██╔═══╝ ╚════╝██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
     ██║██║           ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
     ╚═╝╚═╝            ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + " " * 10 + "Automatic IP Address Changer Tool")
    print(Fore.YELLOW + " " * 10 + "=" * 40 + Style.RESET_ALL + "\n")

def display_interfaces(ip_manager: IPManager):
    """Display available network interfaces"""
    print(Fore.GREEN + "\nAvailable Network Interfaces:")
    print(Fore.GREEN + "-" * 30)
    interfaces = ip_manager.available_interfaces
    if not interfaces:
        print(Fore.RED + "No network interfaces found!")
        return
        
    details = ip_manager.get_interface_details()
    for idx, interface in enumerate(interfaces, 1):
        ip = details[interface].get('ip', 'N/A')
        print(f"{Fore.CYAN}{idx}. {Fore.WHITE}{interface} {Fore.YELLOW}(IP: {ip})")

def main():
    print_banner()
    ip_manager = IPManager()
    
    parser = argparse.ArgumentParser(description="Automatic IP Changer Tool")
    parser.add_argument('-i', '--interface', help="Network interface to change IP")
    parser.add_argument('-a', '--auto', action='store_true', help="Auto change IP at intervals")
    parser.add_argument('-t', '--time', type=int, default=60, 
                       help="Time interval in seconds for auto change (default: 60)")
    parser.add_argument('-l', '--list', action='store_true', help="List available interfaces")
    parser.add_argument('-c', '--current', action='store_true', help="Show current IP address")
    
    args = parser.parse_args()
    
    if args.list:
        display_interfaces(ip_manager)
        return
        
    if args.current:
        current_ip = ip_manager.get_current_ip(args.interface)
        if current_ip:
            print(Fore.GREEN + f"\nCurrent IP: {current_ip}")
        else:
            print(Fore.RED + "\nCould not determine current IP")
        return
    
    if args.auto:
        print(Fore.YELLOW + f"\nAuto-changing IP every {args.time} seconds. Press Ctrl+C to stop...")
        try:
            while True:
                success = ip_manager.change_ip(args.interface)
                if success:
                    current_ip = ip_manager.get_current_ip(args.interface)
                    print(Fore.GREEN + f"Current IP: {current_ip}")
                time.sleep(args.time)
        except KeyboardInterrupt:
            print(Fore.RED + "\nStopped auto IP changer")
    else:
        success = ip_manager.change_ip(args.interface)
        if success:
            current_ip = ip_manager.get_current_ip(args.interface)
            print(Fore.GREEN + f"\nNew IP: {current_ip}")

if __name__ == "__main__":
    main()
