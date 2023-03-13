function chargingCurrent() {
    let C = eo / (18*Math.log(D/d));
    return 2*Math.PI*f*C*V*0.001;
}

function maxChargingCurrent() {
    if (km >= cmp) {
        return Icc * cmp;
    }
    else {
        return Icc * km;
    }
}

function reactivePower() {
    let reset_cycle = 0;
    let reset_value = 0;

    let q = []
    for (let i = 0; i <= km; i++) {
        if (reset_cycle == cmp) {
            reset_value = Icc*V*i*0.001;
            reset_cycle = 0;
        }
        else {
            reset_cycle += 1;
        }
		q.push(Icc*V*i*0.001 - reset_value);
	}
    Icc_max = maxChargingCurrent();
    return q;
}

function updateResults() {
    let TP = Math.sqrt( (document.querySelector('#cap').value**2) - (((Math.sqrt(3)**2)*V*(Icc_max/2)*0.001)**2) );
    let TQp = Math.max.apply(null, Q);
    let TQ = TQp * 3 / 2;

    document.getElementById('res1').innerText = TP.toFixed(2);
    document.getElementById('res2').innerText = TQ.toFixed(2);
    document.getElementById('res3').innerText = Icc_max.toFixed(2);
    document.getElementById('res4').innerText = TQp.toFixed(2);
    document.getElementById('res5').innerText = (TQp / 2).toFixed(2);
}