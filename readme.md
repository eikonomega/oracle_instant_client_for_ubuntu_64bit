# DEPRECATED: Do not use. This no longer works and I am not going to be updating it.

## Easy Installation of Oracle Instant Client on Ubuntu/Debian Linux
Version 1.1

If you've ever had to mess with installing and configuring the Oracle Instant 
Client on your Ubuntu/Debian machine, you know that it's a pain in the arse.  

The crux of the problem lies in the fact the Oracle doesn't create 
Ubuntu/Debian compatible packages for their software.  

This repo contains a simple script which will convert the binaries that
Oracle does provide (Redhat rpm) files into Ubuntu/Debian files and then
install them on your system.

Because of way that Oracle licenses their software, you will need to 
download the rpm's for the version that you want from them directly prior
to using the installation script.

**Important: Currently, this only supports 64-bit machines.**  

### Instructions
1. Download the necessary rpm files from Oracle for whatever version you want.
You'll need the 'basic', 'devel', and 'sqlplus' packages.  
The filenames should match the following pattern:
    * oracle-instantclient[version]-basic-[more-version-info].x86_64.rpm
    * oracle-instantclient[version]-devel-[more-version-info].x86_64.rpm
    * oracle-instantclient[version]-sqlplus-[more-version-info].x86_64.rpm

2. Download the `install_oracle_instantclient.py` script.
3. Run it as root, specifying the location of the rpm files as an argument: `sudo python install_oracle_instantclient.py [directory_holding_rpms]`
    * If you have an error, please submit it as an issue.
4. Obtain your sqlnet.ora, tnsnames.ora, and possibly ldap.ora files from your DBA.
5. Place those files into the /usr/lib/oracle/[version you installed]/client64/network/admin directory.

### Warnings
**This utility is provided as-is with absolutely no support.**  
I will not be able to help you if it hoses up your system somehow.

### Further Reading
This program basically automates the instructions found on the [Ubuntu help forums](https://help.ubuntu.com/community/Oracle%20Instant%20Client).
