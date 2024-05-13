"use strict";
!function () {
    function e() {
        document.querySelector("#RGB").style.background = "rgb(" + i.getValue() + "," + n.getValue() + "," + l.getValue() + ")"
    }

    new Slider("#ex1", {
        formatter: function (e) {
            return "value: " + e
        }
    }), new Slider("#ex2", {});
    var i = new Slider("#R", {reversed: !0}).on("slide", e), n = new Slider("#G", {reversed: !0}).on("slide", e),
        l = new Slider("#B", {reversed: !0}).on("slide", e),
        t = (new Slider("#ex4", {reversed: !0}), new Slider("#ex5"));
    new Slider("#ex6").on("slide", function (e) {
        document.getElementById("ex6SliderVal").textContent = e
    });
    var r = new Slider("#ex7");
    document.querySelector("#ex7-enabled").addEventListener("click", function () {
        this.checked ? r.enable() : r.disable()
    }), new Slider("#ex8", {tooltip: "always"}), new Slider("#ex9", {
        precision: 2,
        value: 8.115
    }), new Slider("#ex10", {}), new Slider("#ex11", {
        step: 2e4,
        min: 0,
        max: 2e5
    }), new Slider("#ex12a", {id: "slider12a", min: 0, max: 10, value: 5}), new Slider("#ex12b", {
        id: "slider12b",
        min: 0,
        max: 10,
        range: !0,
        value: [3, 7]
    }), new Slider("#ex12c", {
        id: "slider12c",
        min: 0,
        max: 10,
        range: !0,
        value: [3, 7]
    }), new Slider("#ex13", {
        ticks: [0, 10, 20, 30, 40],
        ticks_labels: ["$0", "$10", "$20", "$30", "$40"],
        ticks_snap_bounds: 95
    }), new Slider("#ex14", {
        ticks: [0, 10, 20, 30, 40],
        ticks_positions: [0, 30, 60, 80, 100],
        ticks_labels: ["$0", "$10", "$20", "$30", "$40"],
        ticks_snap_bounds: 95
    }), new Slider("#ex15", {min: 1e3, max: 1e7, scale: "logarithmic", step: 10}), new Slider("#ex16a", {
        min: 0,
        max: 10,
        value: 0,
        focus: !0
    }), new Slider("#ex16b", {min: 0, max: 10, value: [0, 10], focus: !0}), new Slider("#ex17a", {
        min: 0,
        max: 10,
        value: 0,
        tooltip_position: "bottom"
    }), new Slider("#ex17b", {
        min: 0,
        max: 10,
        value: 0,
        orientation: "vertical",
        tooltip_position: "left"
    }), new Slider("#ex18a", {min: 0, max: 10, value: 5, labelledby: "ex18-label-1"}), new Slider("#ex18b", {
        min: 0,
        max: 10,
        value: [3, 6],
        labelledby: ["ex18-label-2a", "ex18-label-2b"]
    }), new Slider("#ex22", {
        id: "slider22",
        min: 0,
        max: 20,
        step: 1,
        value: 14,
        rangeHighlights: [{start: 2, end: 5, class: "category1"}, {start: 7, end: 8, class: "category2"}, {
            start: 17,
            end: 19
        }, {start: 17, end: 24}, {start: -3, end: 19}]
    }), new Slider("#ex23", {
        ticks: [0, 1, 2, 3, 4],
        ticks_positions: [0, 30, 70, 90, 100],
        ticks_snap_bounds: 200,
        formatter: function (e) {
            return "value: " + e
        },
        ticks_tooltip: !0,
        step: .01
    }), new Slider("#ex24")
}();