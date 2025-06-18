#!/usr/bin/env python3
from ip_manager import IPManager
from colorama import Fore, Style
import time

def display_menu():
    """Display the interactive menu"""
    print(Fore.YELLOW + "\n" + "=" * 50)
    print(Fore.CYAN + "IP Changer Interactive Mode")
    print(Fore.YELLOW + "=" * 50)
    print(Fore.GREEN + "1. List Available Interfaces")
    print(Fore.GREEN + "2. Show Current IP Address")
    print(Fore.GREEN + "3. Change IP Address")
    print(Fore.GREEN + "4. Auto-Change IP at Intervals")
    print(Fore.RED + "5. Exit")
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def get_interface_choice(ip_manager):
    """Let user select an interface"""
    interfaces = ip_manager.available_interfaces
    if not interfaces:
        print(Fore.RED + "No network interfaces found!")
        return None
    
    print(Fore.CYAN + "\nAvailable Interfaces:")
    for idx, interface in enumerate(interfaces, 1):
        print(f"{Fore.YELLOW}{idx}. {Fore.WHITE}{interface}")
    
    while True:
        try:
            choice = int(input(Fore.CYAN + "\nSelect interface (1-{}): ".format(len(interfaces))))
            if 1 <= choice <= len(interfaces):
                return interfaces[choice-1]
            print(Fore.RED + "Invalid choice!")
        except ValueError:
            print(Fore.RED + "Please enter a number!")

def interactive_mode():
    """Run the interactive console interface"""
    ip_manager = IPManager()
    
    while True:
        display_menu()
        try:
            choice = input(Fore.CYAN + "\nEnter your choice (1-5): " + Style.RESET_ALL)
            
            if choice == "1":
                interfaces = ip_manager.available_interfaces
                details = ip_manager.get_interface_details()
                print(Fore.GREEN + "\nAvailable Network Interfaces:")
                print(Fore.GREEN + "-" * 40)
                for interface in interfaces:
                    info = details.get(interface, {})
                    print(f"{Fore.CYAN}Interface: {Fore.WHITE}{interface}")
                    print(f"  {Fore.YELLOW}IP: {info.get('ip', 'N/A')}")
                    print(f"  {Fore.YELLOW}MAC: {info.get('mac', 'N/A')}")
                    print(f"  {Fore.YELLOW}Netmask: {info.get('netmask', 'N/A')}")
                    print(Fore.GREEN + "-" * 40)
                    
            elif choice == "2":
                interface = get_interface_choice(ip_manager)
                if interface:
                    current_ip = ip_manager.get_current_ip(interface)
                    if current_ip:
                        print(Fore.GREEN + f"\nCurrent IP on {interface}: {current_ip}")
                    else:
                        print(Fore.RED + f"\nCould not determine IP for {interface}")
            
            elif choice == "3":
                interface = get_interface_choice(ip_manager)
                if interface:
                    success = ip_manager.change_ip(interface)
                    if success:
                        new_ip = ip_manager.get_current_ip(interface)
                        print(Fore.GREEN + f"\nIP changed successfully on {interface}")
                        print(Fore.GREEN + f"New IP: {new_ip}")
                    else:
                        print(Fore.RED + f"\nFailed to change IP on {interface}")
            
            elif choice == "4":
                interface = get_interface_choice(ip_manager)
                if interface:
                    try:
                        interval = int(input(Fore.CYAN + "Enter interval in seconds: " + Style.RESET_ALL))
                        print(Fore.YELLOW + f"\nAuto-changing IP every {interval} seconds. Press Ctrl+C to stop...")
                        try:
                            while True:
                                success = ip_manager.change_ip(interface)
                                if success:
                                    current_ip = ip_manager.get_current_ip(interface)
                                    print(Fore.GREEN + f"\n[{time.ctime()}] IP changed to: {current_ip}")
                                time.sleep(interval)
                        except KeyboardInterrupt:
                            print(Fore.RED + "\nStopped auto IP changer")
                    except ValueError:
                        print(Fore.RED + "Invalid interval! Must be a number.")
            
            elif choice == "5":
                print(Fore.YELLOW + "\nExiting IP Changer...")
                break
                
            else:
                print(Fore.RED + "\nInvalid choice! Please select 1-5.")
                
        except KeyboardInterrupt:
            print(Fore.RED + "\nOperation cancelled by user")
            break
        except Exception as e:
            print(Fore.RED + f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    print(Fore.CYAN + "Starting IP Changer Interactive Mode...")
    interactive_mode()
