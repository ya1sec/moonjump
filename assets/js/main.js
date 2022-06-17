$(document).ready(function(){
	var a = {}

	a.clock = {
		init: function() {
			this.tick();
		},

		tick: function() {
			with (new Date()) {
				var h, m, s;

				h = 30 * ((getHours() % 12) + getMinutes() / 60);
				m = 6 * getMinutes();
				s = 6 * getSeconds();

				$('.h_pointer').attr('transform', 'rotate(' + h + ', 50, 50)');
				$('.m_pointer').attr('transform', 'rotate(' + m + ', 50, 50)');
				$('.s_pointer').attr('transform', 'rotate(' + s + ', 50, 50)');

				setTimeout(a.clock.tick, 1000);
			}
		}
	}

// a.setup.init();
a.clock.init();

});
