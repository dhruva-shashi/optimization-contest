function make_submission() {
    if (!document.getElementById('code-file').files[0]) {
        alert('Please upload code file');
        return ;
    }

    if (document.getElementById('code-file').files[0].size > 20000) {
        alert('Code file is too big');
        document.getElementById('submission').reset();
        return ;
    }

    var number_of_empty_files = 0;

    for (var i = 1; i <= 5; i++) {
        if (!document.getElementById('file'+i).files[0])
            number_of_empty_files += 1;
        else if (document.getElementById('file'+i).files[0].size > 10000) {
            alert('File '+i+' is too big');
            document.getElementById('submission').reset();
            return ;
        }
    }

    if (number_of_empty_files == 5) {
        alert('Please upload at least one output file');
        return ;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/submission");

    xhr.onload = function(event) {
        if ('error' in JSON.parse(event.target.response)) {
            alert(JSON.parse(event.target.response)['error']);
            return ;
        }

        alert('Submission received succesfully and is under evaluation');
    };

    var formData = new FormData(document.getElementById("submission"));
    formData.append('passcode', document.getElementById('passcode').value)

    xhr.send(formData);

    document.getElementById('submission').reset();
}

function verify() {
    passcode = document.getElementById('passcode').value;

    document.getElementById('my-submissions').href = '/my-submissions?passcode='+passcode;

	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open("GET", `/get-teamname?passcode=${passcode}`, false);
	xmlHttp.send(null);

	var data = JSON.parse(xmlHttp.responseText);

	if (data['ok']) {
	    document.getElementById('verify').value = 'Verified';
	    document.getElementById('verify').disabled = true;
	    document.getElementById('passcode').disabled = true;

        var best_score = 0;

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", `/best-score?passcode=${passcode}`, false);
        xmlHttp.send(null);

        var best_points = JSON.parse(xmlHttp.responseText)['score'];

        for (var i = 0; i < 5; i++) {
            document.getElementById('best-points-'+(i+1)).innerHTML = best_points[i];
            best_score += best_points[i];
        }

        document.getElementById('best-total-points').innerHTML = best_score;

	    document.cookie = passcode;
	    alert('Logged in as: '+data['teamname']);
	}
    else
        alert(data['error'])
}

function init() {
    if (document.cookie != '') {
        document.getElementById('passcode').value = document.cookie;
	    document.getElementById('verify').disabled = true;
	    document.getElementById('passcode').disabled = true;

	    verify();
    }
}



