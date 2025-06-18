# 🌐 Universal IP Changer Tool
**Developed by**: Pabit (https://github.com/pabit143/Ip-Changer.git)  
**Version**: 2.0  
**License**: MIT  

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)  
![Platforms](https://img.shields.io/badge/Platforms-Linux%20%7C%20Termux%20%7C%20Windows-green)  
![GitHub stars](https://img.shields.io/github/stars/yourusername/ip-changer?style=social)

---

## 📦 Installation

### Linux (Debian/Ubuntu)
```bash
# Install dependencies
sudo apt update && sudo apt install python3 python3-pip git -y

** Clone and install**
git clone https://github.com/yourusername/ip-changer.git
cd ip-changer
pip3 install -r requirements.txt
sudo python3 setup.py install

**First run**
pkg update && pkg install python git -y

 **Then install tool**
git clone https://github.com/yourusername/ip-changer.git
cd ip-changer
pip install -r requirements.txt
python setup.py install --user

**# List interfaces**
ipchanger -l

**# Show current IP**
ipchanger -c

**# List interfaces**
ipchanger -l

**# Show current IP**
ipchanger -c

**# Change IP (default interface)**
ipchanger
