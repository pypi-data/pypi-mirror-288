








<script>


////
///
//
import Panel from '$lib/trinkets/panel/trinket.svelte'
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { find_transaction_by_hash } from '$lib/PTO/Transaction/find_by_hash'
import { fiberize_transaction } from '$lib/PTO/Transaction/Fiberize'
//
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
import { ConicGradient } from '@skeletonlabs/skeleton';
//
//\
//\\

import { onMount, onDestroy } from 'svelte'
import { check_roomies_truck, monitor_roomies_truck } from '$lib/Roomies/Trucks'

let RT_Prepared = "no"
let RT_Monitor;
let RT_Freight;
onMount (async () => {
	const Truck = check_roomies_truck ()
	RT_Freight = Truck.freight; 
	
	RT_Monitor = monitor_roomies_truck ((_freight) => {
		RT_Freight = _freight;
	})
	
	RT_Prepared = "yes"
});

onDestroy (() => {
	RT_Monitor.stop ()
}); 

	
const trends = {
	article: parse_styles ({
		padding: '.3cm',
		'font-size': '2em'
	})
}

let transaction_hash = ""
let transaction_object = ""
const ask_for_transaction = async () => {
	// const warehouse = friends_has_stand.warehouse ()
	// const net_path = RT_Freight.net_path;
	
	const { enhanced } = await find_transaction_by_hash ({
		net_path: RT_Freight.net_path,
		transaction_hash
	})
	const transaction_fiberized = fiberize_transaction ({ transaction: enhanced })
	transaction_object = transaction_fiberized;
}
	
</script>



<div class="card p-8">
	<header style="{parse_styles ({
		padding: '.3cm',
		'font-size': '2em',
		'text-align': 'center'
	})}">Transaction Search</header>  
	
	<div style="height: 0.5cm" />
	
	<div
		style="{parse_styles ({
			display: 'flex',
			'justify-content': 'center'
		})}"
	>

		
		<textarea 
			bind:value={ transaction_hash }
			style="
				padding: .3cm;
			"
			class="textarea" 
			rows="1" 
			placeholder="Transaction Hash" 
		/>
		
		<div style="width: 0.3cm" />


		<button 
			on:click={ ask_for_transaction }
			type="button" 
			class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			style="height: 40px"
		>Ask for Details</button>
	</div>
	
	{#if transaction_object.length >= 1}
	<div
		class="card p-4 variant-soft-primary"
		style="
			margin-top: 10px;
			white-space: pre-wrap;
			word-wrap: break-word;
		"
	><p>{ transaction_object }</p></div>
	{/if}
</div>