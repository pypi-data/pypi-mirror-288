


<script>

import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
	
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
	
///
//
export let unsigned_tx_hexadecimal_string;
export let unsigned_tx_stringified;
export let unsigned_tx_scanned;
//
//\

let unsigned_tx = ""

let current_tab = 0;

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
	
	freight.current.land = "Unsigned_Transaction"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});

</script>


{#if prepared === "yes" }
<div>
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
		>Transaction Petition</header>
		<p>This transaction petition should be the same as the one that was created on the other trinket.</p>
	</div>
	
	<TabGroup>
		<Tab bind:group={ current_tab } name="tab1" value={0}>
			<span longevity="UT_object_button">Object</span>
		</Tab>
		<Tab bind:group={ current_tab } name="tab2" value={1}>
			<span longevity="UT_hexadecimal_string_button">Hexadecimal String</span>
		</Tab>
		
		<svelte:fragment slot="panel">
			{#if current_tab === 0}
				<div>
					<header
						style="
							text-align: center;
							font-size: 1.5em;
							padding: .5cm 0;
						"
					>Object</header>
					<div style="text-align: center">
						<p>For the purpose of showing the object,</p>
						<p>Variables of type <b>Uint8Array</b> were converted into type <b>hexadecimal</b>.</p>
						<p>Variables of type <b>BigInts</b> were converted into type <b>string</b>.</p>
						<div style="height: 8px"></div>
						<p>Those conversions were not applied to the Hexadecimal.</p>
					</div>
					
					<div unsigned_transaction_fiberized>
						<Code_Wall 
							text={ freight.Unsigned_Transaction_Fields.Aptos_object_fiberized } 
						/>
					</div>
				</div>
			{:else if current_tab === 1}
				<div>
					<header
						style="
							text-align: center;
							font-size: 1.5em;
							padding: .5cm 0;
						"
					>Hexadecimal String</header>
					<p
						style="
							text-align: center;
							padding: 10px 0 20px;
						"
					>This is the hexadecimal string of the transaction petition.</p>

					<div unsigned_transaction_hexadecimal_string>
						<Code_Wall 
							text={ freight.Unsigned_Transaction_Fields.hexadecimal_string } 
						/>
					</div>
				</div>
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>
{/if}