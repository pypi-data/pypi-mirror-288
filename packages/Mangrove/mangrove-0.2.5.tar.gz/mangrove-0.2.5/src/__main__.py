'''
__main__.py
Mangrove main file
'''

import os
import sys
import shutil
import argparse
from tabulate import tabulate

from mangrove import magv_config
from mangrove import integrity
from mangrove import install
from mangrove.download_source_support import mangrove
from mangrove.download_source_support import pgxn

'''
Search extension from the source
'''
def search(ext, config):
    try:
        k = pgxn.search(ext, config) + mangrove.search(ext, config)
        if len(k) == 0:
            print("Extension not found.")
            exit(0)
        return k
    except Exception as e :
        config.logger.error(f"Failed to search {ext}")
        config.logger.error(f"e")
        exit(1)

'''
Guide the user to download the extension
'''
def searchdownload(ext, config):
    try:
        k = pgxn.search(ext, config) + mangrove.search(ext, config)
        if len(k) == 0:
            print("Extension not found")
            exit(0)
        print(tabulate(k, headers=['Extension', 'Source', 'Repo', 'Description'], showindex="always"))
        i = 0
        if not len(k) == 1:
            i = secure_input(f"Which extension to download? [0 ~ {len(k)- 1}] ", "int", 0, len(k) - 1)
        return (k[i][0], k[i][1], k[i][2])
    except Exception:
        config.logger.error(f"Failed to download {ext}")
        exit(1)

'''
Download the extension to local
'''
def download(path, ext, branch, source, repo, config):
    if branch == "latest":
        branch = "master"
    try:
        if source == "MANGROVE":
            mangrove.download(path, ext, branch, repo, config)
        elif source == "PGXN":
            pgxn.download(path, ext, branch, config)
        integrity.create_integrity_file(path)
    except Exception:
        config.logger.error(f"Failed to download {ext}")
        exit(1)
    os.chmod(path, 0o777)
'''
Handle the user input
'''
def secure_input(hint, type, lower_bound = 0, upper_bound = 0):
    print(hint)
    if type == "str":
        k = input()
        while k.strip() == "":
            print(hint)
            k = input()
    elif type == "int":
        k = int(input())
        while k > upper_bound or k < lower_bound:
            print(hint)
            try:
                k = int(input())
            except ValueError: # e.g. a float num is given
                k = lower_bound - 1 # So the loop will excute again
    return k

'''
Init the argparse for Mangrove
'''
def initialize_parser():
    parser = argparse.ArgumentParser(description = "Mangrove - PostgreSQL Extension Manager", prog = "mangrove")
    parser.add_argument('-s', '--search', nargs = 1, help="Search extension", metavar = ("extension"))
    parser.add_argument('-d', '--download', nargs = 1, help="Download extension", metavar = ("extension"))
    parser.add_argument('-i', '--install', nargs = 1, help="Install extension", metavar = ("extension"))
    parser.add_argument('-p', '--path', nargs = 1, help = "Specify the download/install path", metavar = "path")
    parser.add_argument('-b', '--branch', nargs = 1, help = "Speicify which branch to download/install", metavar = "branch")
    parser.add_argument('-r', '--root', action = "store_true", help = "Install extension with root permission")
    return parser.parse_args()

'''
The main program
'''
if __name__ == "__main__":
    config = magv_config()
    try:
        if os.path.isfile(os.path.expanduser(config.config["Postscript"])):
            print("Executing initialization script!")
            os.system(f"sh {os.path.expanduser(config.config["Postscript"])}")
    except:
        config.logger.info("Failed to load postscript")

    arg = initialize_parser()
    path_  = arg.path
    
    # Achieve the -b/--branch command
    if not arg.branch == None:
        j = arg.branch[0]
    else:
        j = "latest"

	# Achieve the -s/--search command
    if not arg.search == None:
        print(tabulate(search(arg.search[0], config), headers=['Extension', 'Source', 'Repo', 'Description'], showindex="always"))

	# Achieve the -d/--download command
    if not arg.download == None:
        k = searchdownload(arg.download[0], config)
        if path_ == None:
            path = os.path.join(config.config_path, k[0])
        else:
            path = path_[0]
        try:
            if os.path.isdir(path):
                option = input("Folder already exists, empty the folder? (Y/n)")
                if not (option == 'n' or option == 'N'):
                    shutil.rmtree(path)
            os.makedirs(path, exist_ok = True)
        except:
            config.logger.error(f"Failed to create directory at {path}")
            exit(1)
        download(path, k[0], j, k[1], k[2], config)

	# Achieve the -i/--install command
    if not arg.install == None:
        k = searchdownload(arg.install[0], config)
        choice = 'n'
        if path_ == None:
            path = os.path.join(config.config_path, k[0])
        else:
            path = path_[0]
        if os.path.exists(path):
            if integrity.integrity_check(path, config) == False:
                print("Warning: Integrity check failed, the extension in your local folder might be broken")
                choice = input("Redownload? (y/N) ")
                if (choice == 'y' or choice == 'Y'):
                    try:
                        shutil.rmtree(path)
                        os.makedirs(path, exist_ok = True)
                        download(path, k[0], j, k[1], k[2], config)
                    except:
                        config.logger.error(f"Failed to create directory at {path}")
                        exit(1)
            else:
                choice = input(f"It seems you've already downloaded {k[0]}, install from local? (y/N) ")
                if not (choice == 'y' or choice == 'Y'):
                    try:
                        shutil.rmtree(path)
                        os.makedirs(path, exist_ok = True)
                        download(path, k[0], j, k[1], k[2], config)
                    except:
                        config.logger.error(f"Failed to create directory at {path}")
                        exit(1)
                print("Note: Please make sure the local extension is intact and secure.")
        else:
            os.makedirs(path, exist_ok = True)
            try:
                download(path, k[0], j, k[1], k[2], config)
            except:
                config.logger.error(f"Failed to download at {k[0]}")
                exit(1)
        input("This extension may need higher privilege to install, make sure you give these privilege ")
        try:
            install.install(k[0], k[1], path, config)
        except:
            exit(1)

# no argument in, print the welcome message
if len(sys.argv) == 1:
    print("Mangrove " + config.version)
    print("PostgreSQL Extension Manager")
    print("use 'python -m mangrove -h' get more information.")