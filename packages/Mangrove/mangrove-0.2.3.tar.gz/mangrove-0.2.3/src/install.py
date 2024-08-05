'''
install.py
Install the PostgreSQL extension after download.
'''
import os
import getpass
from subprocess import Popen, PIPE
from tabulate import tabulate

def execute_shell(*shell_scripts):
    shell = ''
    for shell_script in shell_scripts:
        if os.path.isfile(shell_script):
            shell = open(shell_script)
            shell_command = shell.readline()
            while shell_command:
                if os.system(shell_command):
                    return False
                shell_command = shell.readline()
    return True
def install(ext, path, config):
    try:
        if os.path.isfile(os.path.join(path, ".REQUIREMENTS")):
            with open(os.path.join(path, ".REQUIREMENTS")) as f:
                req_list = list(f.read().strip('][').split(', '))
                f.close()
                print("We suggest you install these software, this extension need them to work:")
                for i in range(0, len(req_list)):
                    req_list[i] = req_list[i][1:-1]
                    print(req_list[i], end=' ')
                print("")
                k = input("Installed them? (Y/n) ")
                if k == 'n' or k == 'N':
                    config.logger.info("Warning: force install may work incorrectly")
        os.chdir(path)
        if execute_shell("../magv-index/extension/" + ext + "/pre_install.sh", "../magv-index/extension/" + ext + "/install.sh", "../magv-index/extension/" + ext + "/after_install.sh") is not True:
            raise Exception
    except Exception as e:
        config.logger.error("Installation failed")
        config.logger.error(e)