








<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'

import * as AptosSDK from "@aptos-labs/ts-sdk";

import { ConicGradient } from '@skeletonlabs/skeleton';

import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { ask_latest_block_number } from '$lib/PTO/Blocks/Latest'

import { fiberize_committed_transaction } from '$lib/PTO/Transaction/Committed/Fiberize'
	

const trends = {
	article: parse_styles ({
		padding: '.3cm',
		'font-size': '2em'
	})
}

let address = ""
let transactions_for_address = ""
const ask_for_tx_content = async () => {
	const transactions = await RT_Freight.aptos.getAccountTransactions ({ 
		accountAddress: address 
	});
	if (transactions.length === 0) {
		transactions_for_address = "0 tx found"
		return;
	}
	
	console.log ({ transactions })
	
	// transactions_for_address = JSON.parse ({ transactions })
	transactions_for_address = fiberize_committed_transaction ({ 
		committed_transaction: transactions 
	})
}


import { onMount, onDestroy } from 'svelte'
import {
	check_roomies_truck,
	monitor_roomies_truck
} from '$lib/Roomies/Trucks'

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

	

</script>



<Panel styles={{ "width": "100%" }}>
	<header style="{parse_styles ({
		padding: '.3cm',
		'font-size': '2em',
		'text-align': 'center'
	})}">Transactions</header>  
	
	<div
		style="{parse_styles ({
			display: 'flex',
			'justify-content': 'center'
		})}"
	>
		<div 
			style="height: 40px; background: none; margin-right: 10px"
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
		>
			<div class="input-group-shim">Address</div>
			<input 
				bind:value={ address }
				style="text-indent: 10px" 
				type="text" 
				placeholder="Address" 
			/>
		</div>

		<button 
			on:click={ ask_for_tx_content }
			type="button" 
			class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			style="height: 40px"
		>Ask</button>
	</div>
	
	<div>{ transactions_for_address }</div>
</Panel>