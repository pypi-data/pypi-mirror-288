


<script>


////
///
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
//
import { onMount, onDestroy } from 'svelte';

//
//\
//\\

import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 

let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	freight.current.land = "Transaction_Signature"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
});

onDestroy (() => {
	Truck_Monitor.stop ()
});

let current_show = 0;

</script>

{#if prepared === "yes"}
{#if freight.transaction_signature.hexadecimal_string.length == 0 }
<div
	style="
		padding: 50px
	"
>
	<p>The signature was not added.</p>
</div>
{:else}
<div transaction_signature>
	<div
		style="
			text-align: center;
			padding: 1cm 0 1cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .2cm 0;
			"
		>Transaction Signature</header>
		<p>This Transaction Signature should be the same as the one that was created on the other trinket.</p>
	</div>
	
	<TabGroup>
		<Tab bind:group={current_show} name="tab1" value={0}>
			<span transaction_signature_object>Object</span>
		</Tab>
		<Tab bind:group={current_show} name="tab2" value={1}>
			<span transaction_signature_hexadecimal_string>Hexadecimal</span>
		</Tab>
		
		<svelte:fragment slot="panel">
			{#if current_show === 0}
			<div>
				<header
					style="
						text-align: center;
						font-size: 1.4em;
						padding: .2cm 0;
					"
				>Transaction Signature Object</header>
				<p
					style="text-align: center"
				>This is the signature that was created from the private key.</p>
				<div>
					<Code_Wall
						text={ freight.transaction_signature.Aptos_object_fiberized }
					/>
				</div>
			</div>
			{:else if current_show === 1}
			<div transaction_signature_hexadecimal_string>
				<Code_Wall
					text={ freight.transaction_signature.hexadecimal_string }
				/>
			</div>
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>
{/if}
{/if}