# Automation
Finalproject

https://www.exploit-db.com/searchsploit
On *nix systems, all you really need is either “CoreUtils” or “utilities” (e.g. bash, sed, grep, awk, etc.), as well as git. These are installed by default on many different Linux distributions, including OS X/macOS.
You can easily check out the git repository by running the following:

$ git clone https://github.com/offensive-security/exploitdb.git /opt/exploit-database

An optional step that will make using SearchSploit easier is to include it into your $PATH.
Example: In the following output, the directory /usr/local/bin is included in the $PATH environment variable:

$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
$

With this in mind, you can then create a symbolic link in the /usr/local/bin directory that points to searchsploit, allowing you to run it without providing the full path:

$ ln -sf /opt/exploit-database/searchsploit /usr/local/bin/searchsploit
$

The last stage is to copy the resource file and edit it to match your system environment so it points to the correct directories:

$ cp -n /opt/exploit-database/.searchsploit_rc ~/
$
$ vim ~/.searchsploit_rc

Each section in the resource file (.searchsploit_rc) is split into sections (such as Exploits, Shellcodes, Papers).

    files_array – A Comma-Separated Value file (files_*.CSV) that contains all the data that relates to that section (such as: EDB-ID, Title, Author, Date Published, etc)
    path_array – This points to the directory where all the files are located. **This is often the only value that needs altering**
    name_array – The value name to display in SearchSploit for that section
    git_array – The remote git location to use to update the local copy
    package_array – The package name to use when there is a package manager available (such as apt or brew)

If you want to include Exploit-DB Papers, you can check out the git repository. Afterwards, edit searchsploit’s resource file so paper’s path_array points to the same directory you just checked out.


pip install art

pip install python-nmap

pip install paramiko

pip install 
