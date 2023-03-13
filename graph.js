let ctx, chart;
let d, D, km, V, cmp, Icc, Icc_max, Q;

const f = 50;
const eo = 2.35;

function makeArr(startValue, stopValue, step) {
    let arr = [];
    for (let i = startValue; i < stopValue; i += step) {
      arr.push(i);
    }
    return arr;
}

function getVoltage(radioVoltage) {
    V = radioVoltage.value / Math.sqrt(3);

    graphRenderer();
}

function getCable(radioCable) {
    let cbl = radioCable.value;
    
    d = cables[cbl][0];
    D = cables[cbl][0] + (2*cables[cbl][1]);

    graphRenderer();
}

function graphRenderer() {
    km = document.querySelector("#km").value;
    cmp = document.querySelector("#cmp").value;

    Icc = chargingCurrent();
    Q = reactivePower();

    chart.data.labels = makeArr(0, km, 1)
    chart.data.datasets[0].data = Q
    chart.update();

    updateResults();
}

function init() {
    ctx = document.getElementById('chart');

    d = cables[800][0];
    D = cables[800][0] + (2*cables[800][1]);
    V = 150 / Math.sqrt(3);

    km = document.querySelector("#km").value;
    cmp = document.querySelector("#cmp").value;

    Icc = chargingCurrent();
    Q = reactivePower();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: makeArr(0, km, 1),
            datasets: [{
                label: 'Q/phase (MVAr)',
                data: Q
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    })
}
init()