from flask import Blueprint, render_template, g, request, abort

from db import db_connect, db_close

bp = Blueprint('compare', __name__, url_prefix="/compare")


@bp.before_request
def _start_db():
    db_connect()


@bp.route('/')
def home():
    targets = g.db.getAllTargets().all()
    if request.args:
        t1, t2, e, c, t = parse_query_string(request.args)
        # Get appropriate experiment based on targets chosen
        experiments1 = g.db.getExperimentsByTarget(t1).all()
        experiments2 = g.db.getExperimentsByTarget(t2).all()
        experiments = sorted([g.db.row_to_dict(e) for e in list(set(experiments1) & set(experiments2))], key=lambda x : x['id'])
        # Get appropriate t-tests based on targets and experiment
        ttests1 = [g.db.row_to_dict(t) for t in g.db.getTTraceSetsByTargetAndExperiment(t1, e).all()]
        ttests2 = [g.db.row_to_dict(t) for t in g.db.getTTraceSetsByTargetAndExperiment(t2, e).all()]
        # Get appropriate correlations based on targets and experiment
        corrs1 = [g.db.row_to_dict(t) for t in g.db.getCorrolationTraceByTargetAndExperiment(t1, e).all()]
        corrs2 = [g.db.row_to_dict(t) for t in g.db.getCorrolationTraceByTargetAndExperiment(t2, e).all()]
        return render_template('compare.html', targets=targets, experiments=experiments,
                               ttests1=ttests1, ttests2=ttests2,
                               correlations1=corrs1, correlations2=corrs2,
                               t1=t1, t2=t2, e=e, c=c, t=t)  # Add in selection markers from query string
    else:
        experiments = g.db.getExperimentsByTarget(1)
        ttests = g.db.getTTraceSetsByTargetAndExperiment(1, 1).all()
        correlations = g.db.getCorrolationTraceByTargetAndExperiment(1, 1).all()
        return render_template('compare.html', targets=targets, experiments=experiments,
                               ttests1=ttests, ttests2=ttests,
                               correlations1=correlations, correlations2=correlations,
                               t1=1, t2=1, e=1, c=[], t=[]) # Add default selection markers


def parse_query_string(query_dict):
    """
    Parse a proprietary query string format.
    :param query_dict: query dictionary provided by flask.
    :return: parsed query string.
    """
    try:
        target1 = int(query_dict['t1'])
        target2 = int(query_dict['t2'])
        experiment = int(query_dict['e'])
        if query_dict['c']:
            correlations = list(map(int, query_dict['c'].split(',')))
        else:
            correlations = []
        if query_dict['t']:
            ttests = list(map(int, query_dict['t'].split(',')))
        else:
            ttests = []
        return target1, target2, experiment, correlations, ttests
    except:
        abort(400)


@bp.teardown_request
def _stop_db(_):
    db_close()
