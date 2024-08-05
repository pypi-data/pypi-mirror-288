






<script>

///
//
import { make_barcode } from '$lib/Barcode/make'
//
import { onMount, onDestroy } from 'svelte';
//
//\


import { 
	refresh_truck, 
	 retrieve_truck, 
	 monitor_truck 
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'


let barcode_element = ""

let prepared = "no"
let Truck_Monitor;
let freight;
onMount (() => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 

	Truck_Monitor = monitor_truck ((freight) => {
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	try {
		make_barcode ({
			barcode_element,
			hexadecimal_string: freight.unsigned_transaction.hexadecimal_string,
			size: 400
		})
	}
	catch (exception) {
		console.error (exception)
	}
	
	prepared = "yes"
});

onDestroy (() => {
	Truck_Monitor.stop ()
});




</script>






<div 
	style="
		height: 100%; 
		overflow: scroll;
		padding: .2cm;
	"
>
	<div
		style="
			text-align: center;
			padding: .3cm 0 .1cm;
		"
	>
		<p>This is the transaction as a QR barcode.</p> 
		<p>At
			<a 
				target="_blank"
				href="/relatives/signatures"
			>
				/relatives/signatures
			</a>
			the transaction barcode can be recorded and signed.
		</p> 
	</div>
		
	<pre
		style="
			display: flex;
			justify-content: center;
		"
	>
		<code id="result" bind:this={ barcode_element }></code>
	</pre>
		
	<div
		style="height: 200px"
	>
	</div>
</div>