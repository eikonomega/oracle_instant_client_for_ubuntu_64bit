#!/usr/bin/python
import os
import sys
import glob
import subprocess
import re


def _install_alien():
    """
    Install the alien package which converts .rpm to .deb files.

    """
    subprocess.check_call(["apt-get", "-y", "install", "alien"])


def _install_libaio1():
    """
    Install the libaio1 package.

    """
    subprocess.check_call(["apt-get", "-y", "install", "libaio1"])


class SystemSetup(object):
    def __init__(self):
        print (
            '###############################################################\n'
            'This program will install and configure the Oracle Instant\n'
            'Client on your system.\n\n'
            'You must run this program as root for it to work correctly.\n'
            'You will be prompted for permission to install software.\n'
            'Say yes if you want the program to work. :)\n\n'
            'Press enter to continue.\n'
            '###############################################################\n')

        self.file_insert_header = (
            '\n################################################\n',
            '# Added by Oracle Instant Client Easy-Install  #\n',
            '# On Github @ bit.ly/XoqtcH                    #\n',
            '################################################\n')

        self.program_completion_message = (
            '\n###############################################################\n'
            'Congratulations, the program completed successfully.\n'
            'Oracle Instant Client should now be correctly installed.\n\n'
            'There are a couple of things that you still need to do.\n'
            '1. Obtain sqlnet.ora, tnsnames.ora, and possibly ldap.ora \n'
            '   from your DBA.\n'
            '2. Place these files into the following directory: \n'
            '   /usr/lib/oracle/11.2/client64/network/admin\n'
            '3. Restart your terminal to load the new environment variables.\n'
            '4. Attempt to connect to your database with sqlplus64.\n'
            '5. Please star this repo on Github if it worked for you. :)\n'
            '6. Submit any issues on Github(http://bit.ly/XoqtcH).\n'
            '###############################################################\n')

        self.rpm_files = {
            'basic': '',
            'devel': '',
            'sqlplus': ''
        }

        raw_input()

    def oracle_setup(self, directory_containing_rpms):
        self.rpm_files['basic'] = glob.glob('{}/oracle*basic*rpm'.format(
            directory_containing_rpms))[0]
        self.rpm_files['devel'] = glob.glob('{}/oracle*devel*rpm'.format(
            directory_containing_rpms))[0]
        self.rpm_files['sqlplus'] = glob.glob('{}/oracle*sqlplus*rpm'.format(
            directory_containing_rpms))[0]

        oracle_version = re.findall(
            u'instantclient-basic-([0-9.]+)', self.rpm_files['basic'])[0]

        _install_alien()
        _install_libaio1()

        subprocess.check_call(['alien', '-iv', self.rpm_files['basic']])
        subprocess.check_call(['alien', '-iv', self.rpm_files['devel']])
        subprocess.check_call(['alien', '-iv', self.rpm_files['sqlplus']])

        with open('/etc/ld.so.conf.d/oracle.conf',
                  'w') as oracle_configuration_file:
            oracle_configuration_file.writelines(self.file_insert_header)
            oracle_configuration_file.write(
                '/usr/lib/oracle/{}/client64/lib\n'.format(oracle_version))

        subprocess.check_call(["sudo", "ldconfig"])

        with open('/etc/profile.d/oracle.sh', 'w') as oracle_env_vars:
            oracle_env_vars.writelines(self.file_insert_header)
            oracle_env_vars.write(
                'export ORACLE_HOME=/usr/lib/oracle/'
                '{}/client64\n'.format(oracle_version))
            oracle_env_vars.write(
                'export TNS_ADMIN=/usr/lib/oracle/'
                '{}/client64/network/admin\n'.format(oracle_version))

        with open('{}/.bashrc'.format(os.environ['HOME']), 'a') as bashrc:
            bashrc.writelines(self.file_insert_header)
            bashrc.write('export LD_LIBRARY_PATH=/usr/lib/oracle/'
                         '{}/client64/lib\n'.format(oracle_version))
            bashrc.write('export ORACLE_HOME=/usr/lib/oracle/'
                         '{}/client64\n'.format(oracle_version))
            bashrc.write('export TNS_ADMIN=/usr/lib/oracle/'
                         '{}/client64/network/admin\n'.format(oracle_version))

        os.makedirs(
            '/usr/lib/oracle/{}/client64/network/admin'.format(oracle_version))


if __name__ == '__main__':
    setup = SystemSetup()
    setup.oracle_setup(sys.argv[1])
    print setup.program_completion_message
