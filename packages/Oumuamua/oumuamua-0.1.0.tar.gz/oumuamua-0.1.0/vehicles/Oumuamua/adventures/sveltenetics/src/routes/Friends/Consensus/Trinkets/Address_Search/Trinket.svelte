

<script>

//	import Balance_Trinket from '$lib/trinkets/Consensus/Balance/Trinket.svelte'

import Panel from '$lib/trinkets/panel/trinket.svelte'
import { SlideToggle } from '@skeletonlabs/skeleton';
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { ask_APT_count } from '$lib/PTO/APT/Count'

import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
	

let address_hexadecimal_string = ""
let balance = ""

let Octa_count = ""
let APT_count = ""
let table_opacity = 0

let ask_balance_exception = ""

$: asking = false;


const ask_balance = async () => {
	try {
		console.log ({ RT_Freight }, RT_Freight.net)
		
		const { Octa_count: Octa_count_, APT_count } = await ask_APT_count ({ 
			address_hexadecimal_string,
			net_path: RT_Freight.net_path
		})
		Octa_count = parse_with_commas (Octa_count_);
		table_opacity = 1;
		ask_balance_exception = ""
		
		console.log ({
			Octa_count_,
			APT_count
		})
	}
	catch (_exception) {
		console.error (_exception)
		console.error (_exception.message.toString ())
		
		ask_balance_exception = _exception.message.toString ();
		return;
	}
}

const address_changed = () => {
	table_opacity = 0
	Octa_count = ""
	let APT_count = ""
	ask_balance_exception = ""
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


<Panel 
	styles={{ 
		"width": "100%",
		"padding": "1cm"
	}}
>
	<div style="height: 1cm"></div>

	<header style="{parse_styles ({
		padding: '0',
		'font-size': '2em',
		'text-align': 'center'
	})}">Address Search</header>  
	
	<div style="height: 1cm"></div>
	
	<div
		style="{parse_styles ({
			display: 'flex',
			'justify-content': 'center'
		})}"
	>
		<textarea 
			bind:value={ address_hexadecimal_string }
			on:input={ address_changed }
		
			style="
				padding: .3cm;
			"
			class="textarea" 
			rows="1" 
			placeholder="Address" 
		/>
	
		<div style="width: 0.3cm" />

		<button 
			on:click={ ask_balance }
			type="button" 
			class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			style="height: 40px"
		>Ask for Details</button>
	</div>
	
	<div style="height: 10px"></div>
	
	{#if ask_balance_exception.length >= 1 }
		<aside class="alert variant-ghost">
			<div class="alert-message">
				<p>{ask_balance_exception}</p>
			</div>
		</aside>
	{/if}
	
	<div style="height: 10px"></div>
	
	<div class="table-container"
		style="opacity: { table_opacity }"
	>
		<table class="table table-hover">
			<tbody>
				<tr>
					<td>Octa Balance</td>
					<td>{ Octa_count }</td>
				</tr>
			</tbody>
		</table>
	</div>
</Panel>