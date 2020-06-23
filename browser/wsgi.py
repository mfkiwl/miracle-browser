import logging as log
import os
import sys
import argparse

from flask import Flask
from waitress import serve

sys.path.append(os.path.expandvars("$MIR_DB_REPO_HOME"))

from config import DefaultConfig

def build_arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("db_path",type=str,
        help="path to the database to open")
    
    parser.add_argument("--db-backend",type=str,default="sqlite",
        help="Database backend to use")

    return parser


def create_app(args):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Load the application configuration
    app.config.from_object(DefaultConfig(
        args.db_path,
        db_backend = args.db_backend
    ))

    log.basicConfig(level=app.config["LOG_LEVEL"])

    log.info("Database file: '%s'" % app.config["DB_PATH"])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import pages
    app.register_blueprint(pages.bp)
    app.add_url_rule('/', endpoint="index")

    import targets
    app.register_blueprint(targets.bp)

    import experiments
    app.register_blueprint(experiments.bp)

    import plot
    app.register_blueprint(plot.bp)

    return app


def main():

    parser  = build_arg_parser()
    args    = parser.parse_args()

    app     = create_app(args)
    serve(app)


if (__name__ == "__main__"):
    main()
