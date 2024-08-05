



<script>


////
///
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
import { getToastStore } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
import Net_Choices from '$lib/PTO/Nets/Choices.svelte'
//
import Amount_Field from '$lib/trinkets/Amount_Field/Trinket.svelte'
import Address_Qualities_Trinket from '$lib/trinkets/Address_Qualities/Trinket.svelte'
//
import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
//
//\
//\\
import { ask_for_freight } from '$lib/Roomies/Trucks'


let prepared = "no"
let Truck_Monitor;
let freight;
onMount (() => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	//
	//
	//
	//
	freight.current.land = "Transaction_Fields"

	Truck_Monitor = monitor_truck ((freight) => {
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	
	const roomies_freight = ask_for_freight ();
	freight.fields.ICANN_net_path = roomies_freight.net_path;
	freight.fields.net_name = roomies_freight.net_name;
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});


/*
let net_name = ""
const on_change = ({ net }) => {
	net_name = net.name;
	const net_path = net.path;
	
	freight.fields.ICANN_net_path = net.path;
	freight.fields.net_name = net.name;
}
*/

const on_amount_change = ({ 
	effects,
	actual_amount_of_Octas
}) => {
	console.log ("on_amount_change", actual_amount_of_Octas)
	
	if (effects.problem === "") {
		freight.fields.actual_amount_of_Octas = actual_amount_of_Octas;
	}
}


let origin_address_trinket = ""
const on_prepare_origin_address = () => {
	origin_address_trinket.change_address_hexadecimal_string (
		freight.fields.from_address_hexadecimal_string
	)
}
const on_change_origin_address = ({
	effective,
	address_hexadecimal_string,
	exception
}) => {
	freight.fields.from_address_permitted = effective;
	freight.fields.from_address_exception = exception;
	freight.fields.from_address_hexadecimal_string = address_hexadecimal_string;
}


let to_address_trinket = ""
const on_prepare_to_address = () => {
	to_address_trinket.change_address_hexadecimal_string (
		freight.fields.to_address_hexadecimal_string
	)
}
const on_change_to_address = ({
	effective,
	address_hexadecimal_string,
	exception
}) => {
	freight.fields.to_address = effective;
	freight.fields.to_address = exception;
	freight.fields.to_address_hexadecimal_string = address_hexadecimal_string;
}




</script>


<style>

td {
	display: flex;
	flex-direction: column;
}

p {
	white-space: normal;
}

</style>

{#if prepared === "yes"}
<div>
	<div 
		style="padding: 0.5cm 0"
	>
		<p
			style="text-align: center; font-size: 1em"
		>This is for transfering Octas from one address to another address.</p>
	</div>
	
	<div class="card variant-soft-primary p-4" style="color: inherit">		
		<div
			style="
				display: grid;
				gap: 0.1cm;
				grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Contract</span>
				<span class="badge variant-filled-surface">0x1::aptos_account::transfer</span>
			</span>
		</div>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft-primary p-4" style="color: inherit">
		<header 
			style="
				text-align: center; 
				font-size: 1.2em; 
				font-weight: bold;
				padding: 0 0 8px;
			"
		>ICANN/IANA Net</header>
		
		<div
			style="
				display: grid;
				gap: 0.1cm;
				grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
			"
		>
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Name</span>
				<span class="badge variant-filled-surface">{ 
					freight.fields.net_name
				}</span>
			</span>
			
			<span class="badge variant-soft"
				style="
					position: relative;
					font-size: 1.2em;
				"
			>
				<span>Path</span>
				<span class="badge variant-filled-surface">{ 
					freight.fields.ICANN_net_path
				}</span>
			</span>
		</div>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft-primary p-4" style="color: inherit">
		<Address_Qualities_Trinket 
			name="From Address"
			bind:this={ origin_address_trinket }
			on_change={ on_change_origin_address }
			on_prepare={ on_prepare_origin_address }
		/>
	</div>
	
	<div style="height: 0.5cm"></div>
		
	<div class="card variant-soft-primary p-4" style="color: inherit">
		<Address_Qualities_Trinket 
			name="To Address"
			bind:this={ to_address_trinket }
			on_change={ on_change_to_address }
			on_prepare={ on_prepare_to_address }
		/>
	</div>

	<div style="height: 0.5cm"></div>

	<div class="card variant-soft-primary p-4" style="color: inherit">
		<header 
			style="
				text-align: center; 
				font-size: 1.2em; 
				font-weight: bold;
				padding: 0;
			"
		>Amount</header>
		<p
			style="text-align: center; padding-bottom: 10px"
		>1 APT = 1e8 Octas</p>
		
		<Amount_Field 
			on_change={ on_amount_change }
		/>
	</div>

	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft-primary p-4" style="color: inherit">
		<header
			style="
				text-align: center; 
				font-size: 1.2em; 
				font-weight: bold;
				padding: 10px 0;
			"
		>Transaction Expiration, in seconds</header>
		<label class="label"
			style="display: flex; align-items: center;"
		>
			<input 
				class="input"
				style="text-indent: 10px; padding: 10px" 
				
				transaction_expiration
				placeholder="" 
				
				type="number" 
				bind:value={ freight.fields.transaction_expiration }
			/>
		</label>
	</div>

	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft-primary p-4" style="color: inherit">
		<header 
			style="
				text-align: center; 
				font-size: 1.2em; 
				font-weight: bold;
				padding: 10px 0;
			"
		>Gas Unit Price, in Octas</header>
		<label class="label"
			style="display: flex; align-items: center;"
		>
			<input 
				class="input"
				style="text-indent: 10px; padding: 10px" 
				
				transaction_expiration
				placeholder="" 
				
				type="number" 
				bind:value={ freight.fields.gas_unit_price }
			/>
		</label>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft-primary p-4" style="color: inherit">
		<header
			style="
				text-align: center; 
				font-size: 1.2em; 
				font-weight: bold;
				padding: 10px 0;
			"
		>Max Gas Amount, in Octas</header>
		<label class="label"
			style="display: flex; align-items: center;"
		>
			<input 
				class="input"
				style="text-indent: 10px; padding: 10px" 
				
				transaction_expiration
				placeholder="" 
				
				type="number" 
				bind:value={ freight.fields.max_gas_amount }
			/>
		</label>
	</div>
</div>
{/if}