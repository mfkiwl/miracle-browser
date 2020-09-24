
import os
import subprocess
import logging as log

class DefaultConfig(object):
    """
    The default application configuration object.
    """

    def __init__(self, db_path, db_backend="sqlite"):

        self.LOG_LEVEL = log.INFO

        # Where to open the database connection from.
        self.DB_PATH  = db_path

        # Database engine backend.
        self.DB_BACKEND = db_backend

        # Git commit of the current running version.
        self.GIT_COMMIT = self.__getGitCommit()


    def __getGitCommit(self):
        try:
            cmd = ["git","rev-parse","HEAD"]
            out = subprocess.Popen(
                cmd, stdout = subprocess.PIPE
            ).communicate()[0]
            return str(out.strip())[2:-1]
        except Exception as e:
            log.warn("Unable to get git commit.")
            log.warn(str(e))
            return "Unknown"
