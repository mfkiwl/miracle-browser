$(document).ready(function () {
        $('.target').on('change', function () {
            let target1 = $("#target1").val();
            let target2 = $("#target2").val();
            update_experiments(target1, target2);
        });

        $('#experiment').on('change', function () {
            let target1 = $("#target1").val();
            let target2 = $("#target2").val();
            let experiment = $("#experiment").val();
            update_results(target1, target2, experiment);
        });

        $('#plot_button').click(function () {
            corr_ids = new Set();
            $("#correlation1 :checked").each(function (_, checkbox) {
                corr_ids.add(parseInt($(checkbox).val()));
            });
            $("#correlation2 :checked").each(function (_, checkbox) {
                corr_ids.add(parseInt($(checkbox).val()));
            });
            update_plot(Array.from(corr_ids));
        });

        function _write_experiments(experiments) {
            let experiment_list = $("#experiment");
            experiment_list.html('')
            var accumulator = ""
            experiments.forEach(experiment => accumulator +=
                "<option value=\"" + experiment.id + "\">" + experiment.name + " (" + experiment.catagory + ")</option>"
            );
            if (accumulator) {
                experiment_list.attr('disabled', false);
                experiment_list.html(accumulator);
            } else {
                $("#correlation1 tbody").empty();
                $("#correlation2 tbody").empty();
                experiment_list.attr('disabled', true);
                experiment_list.html('');
                $("#plot_button").attr('disabled', true);
            }
        }

        function _write_results(results) {
            $("#correlation1 tbody").empty();
            $("#correlation2 tbody").empty();
            if ((results.correlations_1.length > 0) && (results.correlations_2.length > 0)) {
                results.correlations_1.forEach(element =>
                    $('#correlation1').append(
                        "<tr>" +
                        "<td><input type=\"checkbox\" name=\"selection\" value=\"" + element.statisticTraceid + "\"></td>" +
                        "<td>" + element.id + "</td>" +
                        "<td>" + element.name + "</td>" +
                        "<td>" + element.corrType.split(".")[1] + "</td>" +
                        "</tr>"
                    )
                );
                results.correlations_2.forEach(element =>
                    $('#correlation2').append(
                        "<tr>" +
                        "<td><input type=\"checkbox\" name=\"selection\" value=\"" + element.statisticTraceid + "\"></td>" +
                        "<td>" + element.id + "</td>" +
                        "<td>" + element.name + "</td>" +
                        "<td>" + element.corrType.split(".")[1] + "</td>" +
                        "</tr>"
                    )
                );
                $("#plot_button").attr('disabled', false);
            } else {
                $("#plot_button").attr('disabled', true);
            }
        }

        function _write_plot(png) {
            $("#plot-text").attr('hidden', false);
            $("#plot").attr('src', png);
        }

        function update_experiments(target1, target2) {
            let json = {
                "target1": target1,
                "target2": target2
            };
            $.ajax("/api/compare/experiments", {
                type: "POST",
                data: JSON.stringify(json),
                contentType: "application/json",
                dataType: "json",
                success: function (data) {
                    _write_experiments(data);
                    update_results(target1, target2, $('#experiment').val());
                }
            });
        }

        function update_results(target1, target2, experiment) {
            if (target1 && target2 && experiment) {
                let json = {
                    "target1": target1,
                    "target2": target2,
                    "experiment": experiment
                };
                $.ajax("/api/compare/results", {
                    type: "POST",
                    data: JSON.stringify(json),
                    contentType: "application/json",
                    dataType: "json",
                    success: function (data) {
                        _write_results(data);
                    }
                });
            }
        }

        function update_plot(trace_ids) {
            let json = {
                "type": "correlation",
                "trace_ids": trace_ids
            };
            $.ajax("/api/compare/plot", {
                type: "POST",
                data: JSON.stringify(json),
                contentType: "application/json",
                dataType: "json",
                success: function (data) {
                    let png_src = 'data:image/png;base64,' + data.plot;
                    _write_plot(png_src);
                }
            });
        }
    }
);