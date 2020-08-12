from flask import Blueprint, render_template, g

from db import db_connect, db_close

bp = Blueprint('compare', __name__, url_prefix="/compare")


@bp.before_request
def _start_db():
    db_connect()


@bp.route('/')
def home():
    targets = g.db.getAllTargets().all()
    experiments = g.db.getExperimentsByTarget(1)
    ttests = g.db.getTTraceSetsByTargetAndExperiment(1, 1).all()
    correlations = g.db.getCorrolationTraceByTargetAndExperiment(1,1).all()
    return render_template('compare.html', targets=targets, experiments=experiments,
                           ttests=ttests, correlations=correlations)


@bp.teardown_request
def _stop_db(_):
    db_close()
