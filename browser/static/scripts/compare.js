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

        $('.selector').click(function (event) {
            let table = event.target.id.split('-')[0];
            let action = {
                'all' : true,
                'none' : false
            }[event.target.id.split('-')[1]];
            if (table === 'corr1') {
                $(".corr1-checkbox").attr('checked', action);
            } else if (table === 'corr2') {
                $(".corr2-checkbox").attr('checked', action);
            } else if (table === 'ttest1') {
                $(".ttest1-checkbox").attr('checked', action);
            } else if (table === 'ttest2') {
                $(".ttest2-checkbox").attr('checked', action);
            }
        });

        $('#plot_button').click(function () {
            $('#shared_div').attr('hidden', true);
            var trace_ids = new Set();
            $("#correlation1 :checked").each(function (_, checkbox) {
                trace_ids.add(parseInt($(checkbox).val()));
            });
            $("#correlation2 :checked").each(function (_, checkbox) {
                trace_ids.add(parseInt($(checkbox).val()));
            });
            $("#ttest1 :checked").each(function (_, checkbox) {
                trace_ids.add(parseInt($(checkbox).val()));
            });
            $("#ttest2 :checked").each(function (_, checkbox) {
                trace_ids.add(parseInt($(checkbox).val()));
            });
            update_plot(Array.from(trace_ids));
        });

        $('#share_button').click(function () {
            var base_url = window.location.href.split('?')[0];
            let target1 = $("#target1").val();
            let target2 = $("#target2").val();
            let experiment = $("#experiment").val();
            var correlations = new Set();
            $("#correlation1 :checked").each(function (_, checkbox) {
                correlations.add(parseInt($(checkbox).val()));
            });
            $("#correlation2 :checked").each(function (_, checkbox) {
                correlations.add(parseInt($(checkbox).val()));
            });
            var ttests = new Set();
            $("#ttest1 :checked").each(function (_, checkbox) {
                ttests.add(parseInt($(checkbox).val()));
            });
            $("#ttest2 :checked").each(function (_, checkbox) {
                ttests.add(parseInt($(checkbox).val()));
            });
            base_url += '?t1=' + target1 + '&t2=' + target2 +
                '&e=' + experiment +
                '&c=' + Array.from(correlations).toString() +
                '&t=' + Array.from(ttests).toString()
            $('#shared_link').html(base_url);
            $('#shared_div').attr('hidden', false);
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
                $("#ttest1 tbody").empty();
                $("#ttest2 tbody").empty();
                experiment_list.attr('disabled', true);
                experiment_list.html('');
                $("#plot_button").attr('disabled', true);
            }
            $("#spinners-top").attr('hidden', true);
        }

        function _write_results(results) {
            $("#correlation1 tbody").empty();
            $("#correlation2 tbody").empty();
            $("#ttest1 tbody").empty();
            $("#ttest2 tbody").empty();
            results.correlations_1.forEach(element =>
                $('#correlation1').append(
                    "<tr>" +
                    "<td><input type=\"checkbox\" name=\"selection\" class=\"corr1-checkbox\" value=\"" + element.statisticTraceid + "\"></td>" +
                    "<td>" + element.id + "</td>" +
                    "<td>" + element.name + "</td>" +
                    "<td>" + element.corrType.split(".")[1] + "</td>" +
                    "</tr>"
                )
            );
            results.correlations_2.forEach(element =>
                $('#correlation2').append(
                    "<tr>" +
                    "<td><input type=\"checkbox\" name=\"selection\" class=\"corr2-checkbox\" value=\"" + element.statisticTraceid + "\"></td>" +
                    "<td>" + element.id + "</td>" +
                    "<td>" + element.name + "</td>" +
                    "<td>" + element.corrType.split(".")[1] + "</td>" +
                    "</tr>"
                )
            );
            results.ttests_1.forEach(element =>
                $('#ttest1').append(
                    "<tr>" +
                    "<td><input type=\"checkbox\" name=\"selection\" class=\"ttest1-checkbox\" value=\"" + element.ttraceId + "\"></td>" +
                    "<td>" + element.id + "</td>" +
                    "<td>" + element.targetFreq + "</td>" +
                    "</tr>"
                )
            );
            results.ttests_2.forEach(element =>
                $('#ttest2').append(
                    "<tr>" +
                    "<td><input type=\"checkbox\" name=\"selection\" class=\"ttest2-checkbox\" value=\"" + element.ttraceId + "\"></td>" +
                    "<td>" + element.id + "</td>" +
                    "<td>" + element.targetFreq + "</td>" +
                    "</tr>"
                )
            );
            if ((results.correlations_1.length > 0) && (results.correlations_2.length > 0) ||
                (results.ttests_1.length > 0) && (results.ttests_2.length > 0)) {
                $("#plot_button").attr('disabled', false);
            } else {
                $("#plot_button").attr('disabled', true);
            }
            $("#spinners-top").attr('hidden', true);
        }

        function _write_plot(png) {
            $("#plot").attr('src', png);
            $("#plotResultsModal").modal('show');
            $("#spinners-bottom").attr('hidden', true);
        }

        function update_experiments(target1, target2) {
            $("#spinners-top").attr('hidden', false);
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
                $("#spinners-top").attr('hidden', false);
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
            $("#spinners-bottom").attr('hidden', false);
            let json = {
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