from flask import Blueprint, request, jsonify, g

import schema.api as validation
from db import db_connect, db_close

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.before_request
def _start_db():
    db_connect()


@bp.route('/compare/experiments', methods=['POST'])
def compare_experiments():
    data = request.get_json()
    validation.compare_experiments(data)
    experiments1 = g.db.getExperimentsByTarget(data['target1']).all()
    experiments2 = g.db.getExperimentsByTarget(data['target2']).all()
    experiments = [g.db.row_to_dict(e) for e in list(set(experiments1) & set(experiments2))]
    return jsonify(experiments)


@bp.route('/compare/results', methods=['POST'])
def compare_results():
    data = request.get_json()
    validation.compare_results(data)
    ttests1 = g.db.getTTraceSetsByTargetAndExperiment(
        data['target1'], data['experiment']
    ).all()
    ttests2 = g.db.getTTraceSetsByTargetAndExperiment(
        data['target2'], data['experiment']
    ).all()
    corrs1 = g.db.getCorrolationTraceByTargetAndExperiment(
        data['target1'], data['experiment']
    ).all()
    corrs2 = g.db.getCorrolationTraceByTargetAndExperiment(
        data['target2'], data['experiment']
    ).all()
    json = {
        't_tests_1': [g.db.row_to_dict(t) for t in ttests1],
        't_tests_2': [g.db.row_to_dict(t) for t in ttests2],
        'correlations_1': [g.db.row_to_dict(t) for t in corrs1],
        'correlations_2': [g.db.row_to_dict(t) for t in corrs2],
    }
    return jsonify(json)


@bp.teardown_request
def _stop_db(_):
    db_close()
