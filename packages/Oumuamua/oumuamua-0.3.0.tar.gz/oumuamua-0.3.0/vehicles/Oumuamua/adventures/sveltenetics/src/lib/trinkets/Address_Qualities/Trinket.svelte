

<script>

//	
/*
	import Address_Qualities_Trinket from '$lib/trinkets/Address_Qualities/Trinket.svelte'

	

	let origin_address = {
		effective: "no",
		address_hexadecimal_string: "",
		exception: ""
	}

	const on_change = ({
		effective,
		address_hexadecimal_string,
		exception
	}) => {
		origin_address.effective = effective;
		origin_address.address_hexadecimal_string = address_hexadecimal_string;
		origin_address.exception = exception;
	}
	
	let address_trinket = ""
	const on_prepare = () => {
		address_trinket.change_address_hexadecimal_string ("")
	}

	<Address_Qualities_Trinket 
		bind:this={ address_trinket }
		name="Origin Address"
		on_change={ on_change }
		on_prepare={ on_prepare }
	/>
*/
import Panel from '$lib/trinkets/panel/trinket.svelte'
import { ConicGradient } from '@skeletonlabs/skeleton';
import { SlideToggle } from '@skeletonlabs/skeleton';
import * as AptosSDK from "@aptos-labs/ts-sdk";
import { onMount, onDestroy } from 'svelte'
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { ask_APT_count } from '$lib/PTO/APT/Count'
//
import { loop } from '$lib/taverns/loop'
import {
	check_roomies_truck,
	monitor_roomies_truck
} from '$lib/Roomies/Trucks'
import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
	
//


export let name = "Address"
export let on_change = () => {}
export let on_prepare = () => {}

let address_hexadecimal_string = ""
let balance = ""

let Octa_count = ""
let APT_count = ""
let table_opacity = 0

let alert_exception = ""
let alert_caution = ""
let alert_info = "Waiting for an address."
let alert_proceeds = "no"

$: asking = true;
$: {
	asking;
	
	if (asking === true) {
		suggest_loop.play ()
	}
	else {
		suggest_loop.stop ()
		show_info ({
			info: ""
		})
	}
}

export const change_address_hexadecimal_string = (address) => {
	address_hexadecimal_string = address;
}

const suggest_loop = loop ({
	wait: 2000,
	action: async () => {
		console.info ({ asking })
		
		if (asking === true) {
			ask_balance ()
		}
	}
})

const send_on_change = () => {
	on_change ({
		effective: alert_proceeds,
		address_hexadecimal_string,
				
		exception: alert_exception
	})
}


//
//	
//
//
const show_exception = ({ exception }) => {
	alert_exception = exception;
	alert_caution = ""
	alert_info = ""
	alert_proceeds = "no";
	
	send_on_change ()
}
const show_caution = ({ caution }) => {
	alert_exception = ""
	alert_caution = caution
	alert_info = ""
	alert_proceeds = "no";
	
	send_on_change ()
}
const show_info = ({ info }) => {
	alert_exception = ""
	alert_caution = ""
	alert_info = info
	alert_proceeds = "no";
	
	send_on_change ()
}
const show_proceeds = ({ Octas }) => {
	alert_exception = ""
	alert_caution = ""
	alert_info = ""
	alert_proceeds = "yes";
	
	Octa_count = parse_with_commas (Octas)
	
	send_on_change ()
}

const ask_balance = async () => {
	console.info ("ask_balance")
	
	try {
		if (address_hexadecimal_string.length === 0) {
			show_info ({
				info: "Waiting for an address"
			})
			return;
		}
		
		const address_hexadecimal_string_ask = address_hexadecimal_string;
		const APT_count_ask = await ask_APT_count ({ 
			address_hexadecimal_string: address_hexadecimal_string_ask,
			net_path: RT_Freight.net_path
		})
		
		//
		// if the address changed during the request
		if (address_hexadecimal_string_ask !== address_hexadecimal_string) {
			show_info ({
				info: "searching for address"
			})
			return;
		}
		
		if (APT_count_ask.effective !== "yes") {
			if (APT_count_ask.error_code === "resource_not_found") {
				show_caution ({
					caution: APT_count_ask.exception
				})
				return;
			}
			
			show_exception ({
				exception: APT_count_ask.exception
			})
			return;
		}
		 
		show_proceeds ({
			Octas: APT_count_ask.Octa_count
		})
	}
	catch (_exception) {
		console.error (_exception)
		show_exception ({
			exception: _exception.message
		})
		
		return;
	}
}

const address_changed = () => {
	if (asking === true) {
		show_info ({
			info: "searching for address"
		})
	}
	else {
		show_info ({
			info: ""
		})
	}
}



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
	
	on_prepare ()
	
	suggest_loop.play ()
});

onDestroy (() => {
	RT_Monitor.stop ()
	suggest_loop.stop ()
}); 



</script>


<div
	style="
		width: 100%;
	"
>
	<div
		style="{parse_styles ({
			display: 'flex',
			'justify-content': 'center'
		})}"
	>
		<div 
			style="
				background: none; 
				margin-right: 10px;
				width: 100%;
			"
			
			class="card"
		>
			<div 
			
				style="
					display: grid;
					grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
					gap: 0.2cm;
					
					align-items: center;
					justify-content: space-between;
					
					padding: 4px;
				"
			>
			
				<div
					style="
						display: flex;
						align-items: center;
						justify-content: center;
						
					"
				>
					<div
						style="
							padding: 0 12px;
						"
					>
						<p
							style="
								font-size: 1.2em;
								font-weight: bold;
							"
						>{ name }</p>
					</div>
					
				</div>
				
				
				<div
					class="card"
					style="
						display: flex;
						align-items: center;
						justify-content: center;
						padding: 4px;
					"
				>
					
					
					
				
					<div
						style="
							display: flex;
							align-items: center;
						"
					>
						<SlideToggle 
							bind:checked={ asking }
						/>
					</div>
					<div style="width: 8px;"></div>
					<p>Ask for Details</p>
					
					<div style="width: 8px;"></div>
					
					
					<div
						style="
							width: 0.8cm;
						"
					>
						{#if asking === true }
						<ConicGradient 
							stops={[
								{ color: 'transparent', start: 0, end: 25 },
								{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
							]} 
							spin width="w-6"
						/>
						{:else}
						<div></div>
						{/if}
					</div>

					
					
				</div>
			</div>
			
			<textarea 
				address_hexadecimal_string
			
				bind:value={ address_hexadecimal_string }
				on:input={ address_changed }
			
				style="
					padding: .2cm;
				"
				class="textarea" 
				rows="1" 
				placeholder="Address" 
			/>
		</div>
	</div>
	
	<div
		style="
			display: grid;
			grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
			gap: 4px;
			width: 100%;
			margin: 4px 0;
		"
	>
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.2em;
			"
		>
			<span>Character Count</span>
			<span class="badge variant-filled-surface">{ 
				address_hexadecimal_string.length 
			}</span>
		</span>
		{#if alert_proceeds === "yes" }
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.2em;
			"
		>
			<span>Octas</span>
			<span class="badge variant-filled-surface">{ Octa_count }</span>
		</span>
		{/if}
	</div>
	
	
	
	{#if alert_info.length >= 1 }
		<aside class="alert variant-soft-primary">
			<div class="alert-message">
				<p>{ alert_info }</p>
			</div>
		</aside>
		<div style="height: .1cm"></div>
	{/if}
	
	{#if alert_caution.length >= 1 }
		<aside class="alert variant-filled-warning">
			<div class="alert-message">
				<p
					style="
						white-space: pre-wrap;
						word-wrap: break-word;
					"
				>{alert_caution}</p>
			</div>
		</aside>
		<div style="height: .1cm"></div>
	{/if}
	
	
	{#if alert_exception.length >= 1 }
		<aside class="alert variant-filled-error">
			<div class="alert-message">
				<p
					style="
						white-space: pre-wrap;
						word-wrap: break-word;
					"
				>{alert_exception}</p>
			</div>
		</aside>
		<div style="height: .1cm"></div>
	{/if}
	
	
	
</div>