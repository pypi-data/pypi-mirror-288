




<script>

///
//
import Barcode from './Barcode/Trinket.svelte'
import Hexadecimal from './Hexadecimal/Trinket.svelte'
import AO from './Object/Trinket.svelte'
//
import { make_barcode } from '$lib/Barcode/make'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
//
import { onMount, onDestroy } from 'svelte';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
//
//\


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
	
	freight.current.land = "Transaction_Signature"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});



let current_show = 0;

</script>





{#if prepared === "yes" }
<div 
	longevity="ST"
	style="
		height: 100%; 
		overflow: scroll;
		padding: 0cm;
	"
>
	<div
		style="
			text-align: center;
			padding: 0cm 0 .3cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .3cm 0;
			"
		>Transaction Signature</header>
		<p>
			<span>With a picture of this at </span>
			<a 
				target="_blank"
				href="/relatives/friends"
			>
				/relatives/friends
			</a>
			<span>an ask can be sent to the consensus.</span>
		</p>
	</div>
	
	
	<TabGroup
		justify="justify-center"
	>
		<Tab bind:group={current_show} name="tab2" value={0}>
			<span hexadecimal_button>Object</span>
		</Tab>
		<Tab bind:group={current_show} name="tab1" value={1}>
			<span barcode_button>Barcode</span>
		</Tab>
		<Tab bind:group={current_show} name="tab2" value={2}>
			<span hexadecimal_button>Hexadecimal</span>
		</Tab>
		

		<svelte:fragment slot="panel">
			{#if current_show === 0}
				<AO />
			{:else if current_show === 1}
				<Barcode />
			{:else if current_show === 2}
				<Hexadecimal />
			{/if}
		</svelte:fragment>
	</TabGroup>
			
	
	
	<div
		style="height: 200px"
	>
	</div>
</div>
{/if}