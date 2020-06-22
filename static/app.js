// var wavesurfer = WaveSurfer.create({
//     container: '#waveform',
//     waveColor: 'violet',
//     progressColor: 'purple'
//     //scrollParent: true
// });

// wavesurfer.load('/static/h.wav');

$(document).ready(function() {
	$('.play').click(function() {;
		req = $.ajax({
			url:'/check',
			type:'POST'
		});
		req.done(function(data){
			for ( var i = 0; i < data.length ; i++ ) {
			//setTimeout(function(){console.log("h") }, 500);
			setTimeout(function(){
				req=$.ajax({
					url: '/playWave',
					type: 'POST'
				});
				req.done(function(data) {
					$('#test').html(data);
				});
			}, i*100);
		}
		});
	});

	$('.submit').click(function() {;
		
		var file={
			'file': $('#file').val()
		};
		req = $.ajax({
			url:'/updateFile',
			type:'POST',
			data: JSON.stringify(file),
			contentType: "application/json;charset=utf-8",
        	//url: "/your/flask/endpoint",
          	traditional: "true",
          	//data: JSON.stringify({names}),
          	dataType: "json"
		});
		req.done(function(data){
			console.log("hi");
			//location.reload(true);
			//return render_template('layout_1.html', length = length,form=form[i:])
		});
	});

	$('.reset').click(function() {;
		req = $.ajax({
			url:'/resetWave',
			type:'POST'
		});
		req.done(function(data){
			$('#test').html(data);
		});
	});
});