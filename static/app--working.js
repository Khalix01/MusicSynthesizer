$(document).ready(function() {
	$('.update').click(function() {;
		for ( var i = 0; i < 100 ; i++ ) {
			//setTimeout(function(){console.log("h") }, 500);
			setTimeout(function(){
				req=$.ajax({
					url: '/update',
					type: 'POST'
				});
				req.done(function(data) {
					$('#test').html(data);
				});
			}, 10);
		}
	});
});