

<script>


/*
	import Eternal_1_Progress from '$lib/trinkets/Progress/Eternal_1/Trinket.svelte'
	<Eternal_1_Progress 
		height={ 50 }
		width={ 50 }
		color={ "#FF0000" }
	/>
*/

import Chart from 'chart.js/auto';
import { onMount, onDestroy } from 'svelte'
import { loop } from '$lib/taverns/loop'
	 

export let height = "50"
export let width = "50"
export let color = "#FF0000"

// let wait_color = document.documentElement.classList.contains ("dark") ? "#000000" : "#FFFFFF";

console.log ({ color })

let canvas = ""


// bellow
const smoothies = [
	[ 0, 10, -10, 0 ],
	[ 0, -10, 10, 0 ]
]
const smoothies_2 = [
	[ 0, 0, -5, 0, 10, 0, -10, 0, 5, 0, 0 ],
	[ 0, 0, 5, 0, -10, 0, 10, 0, -5, 0, 0 ],
]

const smoothie_3_line = [ 0, 0, -5, 0, 10, 0, -10, 0, 5, 0, 0 ]
const smoothies_3 = [
	smoothie_3_line.map (entry => { return entry * 1 }),
	smoothie_3_line.map (entry => { return entry * -1 })
]

console.log ({ smoothies_3 })

let bellow = smoothies_3;

const data = {
	labels: bellow [0],
	datasets: [{
		label: 'Looping tension',
		data: bellow,
		fill: false,
		// borderColor: "#FFFFFF",
		borderColor: color,
		borderWidth: 3,
		
		backgroundColor: 'transparent',
		
		tension: 0.5,
		pointRadius: 0
	}]
};

const config = {
	type: 'line',
	data: data,
	options: {
		// responsive: true,
		// maintainAspectRatio: false,
		_animations: {
			tension: {
				duration: 1000,
				easing: 'linear',
				from: 1,
				to: 0,
				loop: true
			},
		},
		scales: {
			x: {
				display: false,
				grid: {
					display: false // Hides the x-axis grid lines
				},
				ticks: {
					display: false // Hides x-axis ticks
				}
			},
			y: {
				display: false,
				grid: {
					display: false // Hides the y-axis grid lines
				},
				ticks: {
					display: false // Hides y-axis ticks
				}
			}
		},
		plugins: {
			legend: {
				display: false // Hide legend
			},
			tooltip: {
				enabled: false // Hide tooltips
			},
			
		}
	},
	__scales: {
		y: {
			min: 0,
			max: 100
		}
	}
};




let occassion = 0;
const loop_1 = loop ({
	wait: 800,
	wait_for_response: "yes",
	action: async () => {
		// console.info ('looping', occassion)
		
		if (canvas instanceof Element !== true) {
			return;
		}
		
		The_Chart.data.datasets [0].data = bellow [ occassion ];
		The_Chart.update ();
		
		occassion += 1
		if (occassion === bellow.length) {
			occassion = 0
		}
	}
})


let The_Chart = ""
onMount (() => {
	const ctx = canvas
	The_Chart = new Chart (ctx, config);
	
	loop_1.play ()
})

onDestroy (() => {
	loop_1.stop ()
})

</script>


<div
	style="
		position: relative;
		width: { width };
		height: { height };
		min-width: 60px;
	"
>
	<canvas
		bind:this={ canvas }
		
		style="
			position: absolute;
			top: 0;
			left: 0;
		
			height: 100% !important;
			width: 100% !important;
		"
	/>
</div>