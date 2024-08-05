




<script>

///
//
//
import Barcode from './Barcode.svelte'
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
//
import { CodeBlock } from '@skeletonlabs/skeleton';
import { getToastStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { clipboard } from '@skeletonlabs/skeleton';
//
import { onMount, onDestroy } from 'svelte';
//
//\

import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
	

import CircleAlert from 'lucide-svelte/icons/circle-alert'

import { build_the_unsigned_transaction } from './build_the_unsigned_transaction'



import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land,
	delete_unsigned_transaction
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
//
//\
//\\




let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	delete_unsigned_transaction ()
	
	//
	//
	//
	//
	freight.current.land = "Unsigned_Transaction"

	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
		
		console.log ("Unsigned Transaction: Truck_Monitor", { _freight })
	})
	
	prepared = "yes"
	
	try {
		await build_the_unsigned_transaction ({ freight })
	}
	catch (exception) {
		console.error (exception)
		freight.unsigned_transaction.exception_text = exception.message;
	}
});

onDestroy (() => {
	Truck_Monitor.stop ()
});


let current_format = 0;


let clone_text = "Clone"
let timeout;
const on_clone = async () => {
	console.log ('on clone')
	
	clearTimeout (timeout)
	
	clone_text = "Cloned"
	
	await new Promise (resolve => {
		timeout = setTimeout (() => {
			resolve ()
		}, 1000)
	})
	
	clone_text = "Clone"
}


</script>





{#if prepared === "yes"}
<div 
	unsigned_transaction_leaf
	style="
		overflow: scroll;
		padding: .2cm;
	"
>
	<div
		style="
			text-align: center;
			padding: 0cm 0;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .5cm 0;
			"
		>Transaction Petition</header>
		<p>A blockchain transaction requires <b>a transaction petition</b> + <b>a transaction signature</b>.</p>
		<p>The transaction can be signed from a "Relatives" trinket by recoding the barcode and then creating a signature from the transaction and a private key.</p>
	</div>
	
	{#if freight.unsigned_transaction.exception_text.length >= 1 }
	<aside 
		class="alert variant-filled-error" 
		style="display: flex; flex-direction: row; margin-bottom: 20px; padding: 25px 20px;"
	>
		<div>
			<CircleAlert />
		</div>
		<p style="margin: 0; padding-left: 10px;">{freight.unsigned_transaction.exception_text}</p>
	</aside>
	{/if}
	
	<div style="height: 12px"></div>
	
	<hr>
	
	<TabGroup justify="justify-center">
		<Tab bind:group={current_format} name="tab1" value={0}>
			<span transaction_as_object_button>Object</span>
		</Tab>
		<Tab bind:group={current_format} name="tab2" value={1}>
			<span transaction_as_hexadecimal_string_button>Hexadecimal</span>
		</Tab>
		<Tab bind:group={current_format} name="tab3" value={2}>
			<span 
				transaction_as_barcode_button
			>Barcode</span>
		</Tab>

		<svelte:fragment slot="panel">
			{#if current_format === 0}
				<div style="text-align: center; padding-bottom: 12px;">
					<p>This is the transaction as an Object.</p>
					<div style="height: 8px"></div>
					<p>For the purpose of showing the object,</p>
					<p>Variables of type <b>Uint8Array</b> were converted into type <b>hexadecimal</b>.</p>
					<p>Variables of type <b>BigInts</b> were converted into type <b>string</b>.</p>
					<div style="height: 8px"></div>
					<p>Those conversions were not applied to the Hexadecimal or Barcode.</p>
				</div>
				
				<div unsigned_transaction_fiberized>
					<Code_Wall 
						text={ freight.unsigned_transaction.Aptos_object_fiberized } 
					/>
				</div>
				
			{:else if current_format === 1}
				<div
					style="
						padding: 0.5cm;
					"
				>
					<p
						style="
							text-align: center;
							padding: 0 0 10px;
						"
					>This is transaction as a hexadecimal string.</p>
					
					
					<div health="UT_Object__UT_hexadecimal_string">
						<Code_Wall 
							can_clone={ "yes" }
							text={ freight.unsigned_transaction.hexadecimal_string } 
						/>
					</div>
				</div>
				
			{:else if current_format === 2}
				<Barcode />
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>
{/if}