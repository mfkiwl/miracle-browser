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

    # Plot 1
    traces, labels = [], []
    for trace_id in data['plot1']:
        stat_trace = g.db.getStatisticTraceById(trace_id)
        traces.append(stat_trace.getValuesAsNdArray())
        labels.append(stat_trace.name)
    figure1 = plotting.makePlotFigure(
        traces,
        slabels=labels,
        xlabel="Sample"
    )
    base64_plot1 = plotting.b64_plot_png(figure1)

    # Optional Plot 2
    if data['mode'] == 'multi' and data.get('plot2'):
        traces, labels = [], []
        for trace_id in data['plot2']:
            stat_trace = g.db.getStatisticTraceById(trace_id)
            traces.append(stat_trace.getValuesAsNdArray())
            labels.append(stat_trace.name)
        figure2 = plotting.makePlotFigure(
            traces,
            slabels=labels,
            xlabel="Sample"
        )
        base64_plot2 = plotting.b64_plot_png(figure2)

        return jsonify({
            'plot1': base64_plot1,
            'plot2': base64_plot2
        })

    return jsonify({
        'plot1': base64_plot1
    })


@bp.teardown_request
def _stop_db(_):
    db_close()
