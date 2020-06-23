
import os
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

