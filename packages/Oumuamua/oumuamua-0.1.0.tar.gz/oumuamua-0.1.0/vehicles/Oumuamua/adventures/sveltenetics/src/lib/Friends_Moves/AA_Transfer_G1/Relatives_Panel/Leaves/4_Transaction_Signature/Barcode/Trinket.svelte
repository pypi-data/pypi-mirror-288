
<script>

import { make_barcode } from '$lib/Barcode/make'
//
import { onMount, onDestroy } from 'svelte';
import { ConicGradient } from '@skeletonlabs/skeleton';
//

import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Logistics/Truck'
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
	
	show_QR_of_signed_tx ({})
});
onDestroy (() => {
	Truck_Monitor.stop ()
});


let showing = "no"
let barcode_element = ""

const show_QR_of_signed_tx = async ({
	loop_limit = 10,
	current_loop = 1
}) => {	
	console.log ("show_QR_of_signed_tx", { current_loop, barcode_element })
	
	if (current_loop === loop_limit) {
		return;
	}
	
	if (typeof barcode_element !== "object") {
		await new Promise (resolve => {
			setTimeout (() => {
				resolve ()
			}, 500)
		})
		
		current_loop = current_loop + 1
		show_QR_of_signed_tx ({
			current_loop
		})
		
		return;
	}
	
	make_barcode ({
		barcode_element,
		hexadecimal_string: freight.Unsigned_Transaction_Signature.hexadecimal_string,
		size: 400
	})
	
	showing = "yes"
}

</script>




{#if prepared === "yes" }
<div>
	{#if showing === "no" }
	<ConicGradient 
		stops={[
			{ color: 'transparent', start: 0, end: 25 },
			{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
		]} 
		spin
		width="w-5"
	/>
	{/if}
	
	<p 
		style="
			text-align: center;
			padding: 20px 0 0;
		"
	>This is the QR barcode equivalent of the signed transaction from the "ST Object" panel.</p> 
	
	<pre
		style="
			display: flex;
			justify-content: center;
		"
	>
		<code 
			bind:this={ barcode_element }
			id="result" 
		></code>
	</pre>
</div>
{/if}