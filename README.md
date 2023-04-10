# Automation
The project is ment to run on a Raspberry Pi in a Cronjob for automatic network scans. The project is using the Telegram application for exfiltration of data. Follow below steps for correct setup (works on all linux distro's).

### INSTALL PACKAGES WITH APT-GET ###

sudo apt-get install net-tools

sudo apt-get install nmap

sudo apt-get install python3-pip

### INSTALL PYTHON PIP LIBRARIES ###

pip install python-nmap

pip install telepot

### INSTALL SEARCHSPLOIT / EXPLOITDB ###

sudo git clone https://github.com/offensive-security/exploit-database.git /opt/exploit-database

/opt/exploit-database/searchsploit -u

### INSTALL SCAN FILES ###

Clone the files to relevant directory you choose

git clone https://github.com/Healthy-byte/Automation.git

### INSTALL TELEGRAM APPLICATION FOR PHONE OR DESKTOP AND SETUP SECRET.PY FILE ###

Add username BotFather and write "/newbot" in the chat. Give it a fitting name and username.
You token should look like this: "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"

In the same directory as the scan files (Automation), create a file called "secrets.py" (touch secrets.py).

Edit the file with a text editor and copy your token into the file like this: 
token = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ" #Change the token example with your own

run the telebot_phone_id.py script to get your chat id, write anything in the Telegram application and save the output to the secrets.py with the var name: chat_id = 12345 #Change the chat ID example with your own
