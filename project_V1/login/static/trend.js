window.onload = function () {

	var options = {
		animationEnabled: true,
		title: {
			text: "Monthly Sales Comparison by Location"
		},
		axisY: {
			title: "Revenue (in Pound Sterling)",
			valueFormatString: "#0",
			suffix: "K",
			prefix: "£",
			linecolor: "#00802b",

		},
		legend: {
			cursor: "pointer",
			itemclick: toogleDataSeries
		},
		toolTip: {
			shared: true
		},
		data: [{
			type: "splineArea",
			color: " #66ff33",
			fillOpacity: .4,
			name: "London",
			markerSize: 7,
			showInLegend: true,
			xValueFormatString: "MMMM",
			yValueFormatString: "£#0K",
			dataPoints: [{
					x: new Date(2017, 0),
					y: 12
				},
				{
					x: new Date(2017, 1),
					y: 15
				},
				{
					x: new Date(2017, 2),
					y: 12
				},
				{
					x: new Date(2017, 3),
					y: 17
				},
				{
					x: new Date(2017, 4),
					y: 20
				},
				{
					x: new Date(2017, 5),
					y: 21
				},
				{
					x: new Date(2017, 6),
					y: 24
				},
				{
					x: new Date(2017, 7),
					y: 19
				},
				{
					x: new Date(2017, 8),
					y: 22
				},
				{
					x: new Date(2017, 9),
					y: 25
				},
				{
					x: new Date(2017, 10),
					y: 21
				},
				{
					x: new Date(2017, 11),
					y: 19
				}
			]
		}, {
			type: "splineArea",
			name: "Manchester",
			markerSize: 5,
			color: " #ff0000",
			fillOpacity: .5,

			showInLegend: true,
			yValueFormatString: "£#0K",
			dataPoints: [{
					x: new Date(2017, 0),
					y: 8
				},
				{
					x: new Date(2017, 1),
					y: 14
				},
				{
					x: new Date(2017, 2),
					y: 9
				},
				{
					x: new Date(2017, 3),
					y: 11
				},
				{
					x: new Date(2017, 4),
					y: 15
				},
				{
					x: new Date(2017, 5),
					y: 12
				},
				{
					x: new Date(2017, 6),
					y: 13
				},
				{
					x: new Date(2017, 7),
					y: 9
				},
				{
					x: new Date(2017, 8),
					y: 7
				},
				{
					x: new Date(2017, 9),
					y: 14
				},
				{
					x: new Date(2017, 10),
					y: 18
				},
				{
					x: new Date(2017, 11),
					y: 14
				}
			]
		}]
	};
	$("#chartContainer").CanvasJSChart(options);

	function toogleDataSeries(e) {
		if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
			e.dataSeries.visible = false;
		} else {
			e.dataSeries.visible = true;
		}
		e.chart.render();
	}

}