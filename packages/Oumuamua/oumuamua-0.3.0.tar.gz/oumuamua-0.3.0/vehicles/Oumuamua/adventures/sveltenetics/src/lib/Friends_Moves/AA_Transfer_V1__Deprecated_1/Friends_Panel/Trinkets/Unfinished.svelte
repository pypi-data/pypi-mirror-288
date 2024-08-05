

<script>

import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
import { onMount, onDestroy } from 'svelte';
import { fade } from 'svelte/transition';

let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
});

onDestroy (() => {
	Truck_Monitor.stop ()
});

const close_the_waiting_modal = () => {
	freight.unfinished_extravaganza.showing = "no"
}

</script>




{#if prepared ==="yes" && freight.unfinished_extravaganza.showing === "yes" }
<div
	transition:fade
	unfinished-extravaganza
	class="card"
	style="
		display: block;
		position: absolute;
		top: 10px;
		left: 10px;
		
		width: calc(100% - 20px);
		height: calc(100% - 90px);
		
		opacity: 1;
		border-radius: 8px;
		
		z-index: 9999;
	"
>
	<div
		style="
			position: absolute;
			top: 0;
			left: 0;
			
			width: 100%;
			height: 100%;
			
			display: flex;
		"
	>
		<main
			style="
			position: absolute;
				top: 0;
				left: 0;
				
				width: 100%;
				height: calc(100% - 60px);
				
				display: flex;
				align-items: center;
				justify-content: center;
			"
		>
			Unfinished
		</main>
		<footer
			style="
				position: absolute;
				bottom: 0;
				left: 0;
			
				height: 60px;
				width: 100%;
				padding: 8px;
				
				display: flex;
				justify-content: right;
			"
		>
			<button class="btn variant-filled" on:click={close_the_waiting_modal}>
				Close
			</button>
		</footer>
	</div>
</div>
{/if}