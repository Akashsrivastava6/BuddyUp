$(function () {
    var totalRevenue = 15341110;

    // CanvasJS column chart to show revenue from Jan 2015 - Dec 2015
    var revenueColumnChart = new CanvasJS.Chart("revenue-column-chart", {
        animationEnabled: true,
        backgroundColor: "transparent",
        theme: "theme2",
        axisX: {
            labelFontSize: 14,
            valueFormatString: "MMM YYYY"
        },
        axisY: {
            labelFontSize: 14,
            prefix: "$"
        },
        toolTip: {
            borderThickness: 0,
            cornerRadius: 0
        },
        data: [{
            type: "column",
            yValueFormatString: "$###,###.##",
            dataPoints: [{
                    x: new Date("1 Jan 2015"),
                    y: 868800
                },
                {
                    x: new Date("1 Feb 2015"),
                    y: 1071550
                },
                {
                    x: new Date("1 Mar 2015"),
                    y: 1286200
                },
                {
                    x: new Date("1 Apr 2015"),
                    y: 1106900
                },
                {
                    x: new Date("1 May 2015"),
                    y: 1033800
                },
                {
                    x: new Date("1 Jun 2015"),
                    y: 1017160
                },
                {
                    x: new Date("1 Jul 2015"),
                    y: 1458000
                },
                {
                    x: new Date("1 Aug 2015"),
                    y: 1165850
                },
                {
                    x: new Date("1 Sep 2015"),
                    y: 1594150
                },
                {
                    x: new Date("1 Oct 2015"),
                    y: 1501700
                },
                {
                    x: new Date("1 Nov 2015"),
                    y: 1588400
                },
                {
                    x: new Date("1 Dec 2015"),
                    y: 1648600
                }
            ]
        }]
    });

    revenueColumnChart.render();

    //CanvasJS pie chart to show product wise annual revenue for 2015
    var productsRevenuePieChart = new CanvasJS.Chart(
        "products-revenue-pie-chart", {
            animationEnabled: true,
            theme: "theme2",
            legend: {
                fontSize: 14
            },
            toolTip: {
                borderThickness: 0,
                content: "<span style='\"' color: {color};'\"'>{name}</span>: ${y} (#percent%)",
                cornerRadius: 0
            },
            data: [{
                indexLabelFontColor: "#676464",
                indexLabelFontSize: 14,
                legendMarkerType: "square",
                legendText: "{indexLabel}",
                showInLegend: true,
                startAngle: 90,
                type: "pie",
                dataPoints: [{
                        y: 6289855,
                        name: "Product A",
                        indexLabel: "Product A - 41%",
                        legendText: "Product A",
                        exploded: true
                    },
                    {
                        y: 2761400,
                        name: "Product B",
                        indexLabel: "Product B - 18%",
                        legendText: "Product B"
                    },
                    {
                        y: 3681866,
                        name: "Product C",
                        indexLabel: "Product C - 24%",
                        legendText: "Product C",
                        color: "#8064a1"
                    },
                    {
                        y: 2607989,
                        name: "Product D",
                        indexLabel: "Product D - 17%",
                        legendText: "Product D"
                    }
                ]
            }]
        }
    );

    productsRevenuePieChart.render();

    //CanvasJS spline chart to show orders from Jan 2015 to Dec 2015
    var ordersSplineChart = new CanvasJS.Chart("orders-spline-chart", {
        animationEnabled: true,
        backgroundColor: "transparent",
        theme: "theme2",
        toolTip: {
            borderThickness: 0,
            cornerRadius: 0
        },
        axisX: {
            labelFontSize: 14,
            maximum: new Date("31 Dec 2015"),
            valueFormatString: "MMM YYYY"
        },
        axisY: {
            gridThickness: 0,
            labelFontSize: 14,
            lineThickness: 2
        },
        data: [{
            type: "spline",
            dataPoints: [{
                    x: new Date("1 Jan 2015"),
                    y: 17376
                },
                {
                    x: new Date("1 Feb 2015"),
                    y: 21431
                },
                {
                    x: new Date("1 Mar 2015"),
                    y: 25724
                },
                {
                    x: new Date("1 Apr 2015"),
                    y: 22138
                },
                {
                    x: new Date("1 May 2015"),
                    y: 20676
                },
                {
                    x: new Date("1 Jun 2015"),
                    y: 25429
                },
                {
                    x: new Date("1 Jul 2015"),
                    y: 29160
                },
                {
                    x: new Date("1 Aug 2015"),
                    y: 23317
                },
                {
                    x: new Date("1 Sep 2015"),
                    y: 31883
                },
                {
                    x: new Date("1 Oct 2015"),
                    y: 30034
                },
                {
                    x: new Date("1 Nov 2015"),
                    y: 31768
                },
                {
                    x: new Date("1 Dec 2015"),
                    y: 41215
                }
            ]
        }]
    });

    ordersSplineChart.render();
});