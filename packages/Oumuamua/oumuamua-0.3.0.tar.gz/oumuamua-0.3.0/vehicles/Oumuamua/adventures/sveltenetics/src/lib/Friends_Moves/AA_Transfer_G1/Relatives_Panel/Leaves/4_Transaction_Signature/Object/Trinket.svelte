
<script>

import { make_barcode } from '$lib/Barcode/make'
//
import { onMount, onDestroy } from 'svelte';
import { ConicGradient } from '@skeletonlabs/skeleton';
//
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
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
});
onDestroy (() => {
	Truck_Monitor.stop ()
});


</script>

{#if prepared === "yes" }
<div aptos_object_signature>
	<Code_Wall
		text={ freight.Unsigned_Transaction_Signature.Aptos_object_fiberized }
		can_clone={ "yes" }
	/>
</div>
{/if}