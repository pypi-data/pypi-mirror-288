'''
integrity.py
Check the integrity of the extension after download to local.
'''
import os
from datetime import datetime
from magv import magv_config

INTEGRITY_FILE = '.INTEGRITY'

def integrity_check(path, config):
    config.logger.info(f"Performing integrity check for {path}")
    try:
        if os.path.isfile(os.path.join(path, INTEGRITY_FILE)) == True:
            config.logger.info("Integrity check passed")
            return True
        else:
            config.logger.error("Integrity check failed")
            return False
    except Exception as e:
        config.logger.error("Integrity check failed. An exception is raised")
        config.logger.error(e)
        return False

'''
Create integrity file means we complete the download work successfully
'''
def create_integrity_file(path):
    with open(os.path.join(path, INTEGRITY_FILE), "w+") as f:
        f.write(f"INTEGRITY CHECK PASSED AT {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}")
        f.close()