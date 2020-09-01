from flask import Blueprint, request, jsonify, g

import processing.plotting as plotting
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
        'ttests_1': [g.db.row_to_dict(t) for t in ttests1],
        'ttests_2': [g.db.row_to_dict(t) for t in ttests2],
        'correlations_1': [g.db.row_to_dict(t) for t in corrs1],
        'correlations_2': [g.db.row_to_dict(t) for t in corrs2],
    }
    return jsonify(json)


@bp.route('/compare/plot', methods=['POST'])
def compare_plots():
    data = request.get_json()
    validation.compare_plots(data)

    traces = []
    labels = []

    for trace_id in data['trace_ids']:
        stat_trace = g.db.getStatisticTraceById(trace_id)
        traces.append(stat_trace.getValuesAsNdArray())
        labels.append(stat_trace.name)

    figure = plotting.makePlotFigure(
        traces,
        slabels=labels,
        xlabel="Sample"
    )

    base64_png = plotting.b64_plot_png(figure)

    return jsonify({
        'plot': base64_png
    })


@bp.teardown_request
def _stop_db(_):
    db_close()
