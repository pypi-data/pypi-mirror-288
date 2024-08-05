
<script>

////
///
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
import Button from '$lib/trinkets/button/trinket.svelte'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { loop } from '$lib/taverns/loop'
//
import { send_coins_from_faucet } from '$lib/PTO/Faucet/send'
import { find_transaction_by_hash } from '$lib/PTO/Transaction/find_by_hash'
//
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
import { Aptos, AptosConfig, Network, Account } from "@aptos-labs/ts-sdk";
//
//\
//\\

import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
	

let to_address_hexadecimal_string = ""
let amount_of_Octas = "1e8"
let actual_amount_of_Octas_string = "100000000"

let faucet_net_path = 'https://faucet.devnet.aptoslabs.com/mint'
let net_path = 'https://api.devnet.aptoslabs.com/v1'



let asking = "no"
let alert_error_text = ""
let alert_message = ""
let transaction_success_message = ""
let transaction_error_message = ""
let transaction_object = ""


const transaction_progress = {
	coin_ask: {
		asked: "no",
		alert_success_text: "",
		alert_error_text: ""
	},
	transaction_ask: {
		asking: "no",
		alert_success_text: "",
		alert_error_text: ""
	}
}


const amount_of_Octas_changed = async () => {
	let amount_of_Octas_in_input = event.target.value;
	let float_amount = parseFloat (amount_of_Octas_in_input)
	
	console.log ({ amount_of_Octas_in_input, float_amount })
	
	actual_amount_of_Octas_string = float_amount.toString ()
}


let transaction_hash = ""

const loop_1 = loop ({
	wait: 2000,
	wait_for_response: "yes",
	action: async () => {
		console.info ("looping")
		
		const { enhanced, transaction_fiberized } = await find_transaction_by_hash ({
			net_path,
			transaction_hash
		})
				
		console.log ({
			enhanced
		})		
				
		if (enhanced.success === true) {
			transaction_success_message = "The transaction was successful."
			transaction_object = transaction_fiberized;
			
			loop_1.stop ()
		}
	}
})



const ask_for_Octas = async () => {
	alert_error_text = ""
	
	try {
		if (to_address_hexadecimal_string.length == 0) {
			alert_error_text = "An Address wasn't choosen."			
			return;
		}
		
		const { tx } = await send_coins_from_faucet ({
			amount: actual_amount_of_Octas_string,
			address: to_address_hexadecimal_string,
			URL: faucet_net_path
		})
		
		alert_message = `
The faucet returned transaction hexadecimal: 
${ tx }
	
Waiting on transaction success confirmation.
		`.trim ();
		
		const action = async () => {
			const { enhanced, transaction_fiberized } = await find_transaction_by_hash ({
				net_path,
				transaction_hash: tx
			})
					
			if (enhanced.success === true) {
				transaction_success_message = "The transaction was successful."
				
				transaction_object = transaction_fiberized;
				return "yes"
			}
			
			return "no"
		}
		transaction_hash = tx;
		
		loop_1.play ()
		const proceeds = await loop ({
			action
		})
		
		if (proceeds != "success") {
			transaction_error_message = "The transaction maybe was not successful."
		}
	}
	catch (exception) {
		transaction_error_message = exception.message;
	}
}

</script>

<Panel styles={{ "width": "100%" }}> 
	<div
		style="
			height: 90vh;
			overflow: scroll;
			padding: 1cm 0.5cm 0;
		"
	>
		<header
			style="text-align: center; font-size: 2em"
		>Faucet</header>
		
		<p style="text-align: center; margin-top: 10px;">
			This is for receiving Octas.  This isn't possible on the mainnet.
		</p>
		
		<hr class="!border-t-4" style="margin: 1cm 0" />
		
		<div class="card variant-soft-primary p-4" style="color: inherit">
			<header style="text-align: center; font-size: 1.5em; padding: 10px 0">Faucet Net Path</header>
			<textarea 
				ican_net_address
				
				bind:value={ faucet_net_path }
				
				class="textarea"
				style="min-height: 50px; padding: 10px"
				type="text" 
				placeholder=""
				
				rows="1"
			/>
		</div>
		
		<div style="height: 0.5cm"></div>
		
		<div class="card variant-soft-primary p-4" style="color: inherit">
			<header style="text-align: center; font-size: 1.5em;">To Address</header>
			<div style="height: 0.5cm"></div>
			<p 
				style="text-align: center;"
			>Example: 522D906C609A3D23B90F072AD0DC74BF857FB002E211B852CE38AD6761D4C8FD</p>
			<div style="height: 0.5cm"></div>
			<textarea 
				to_aptos_address
				class="textarea"
				style="min-height: 50px; padding: 10px"
				bind:value={ to_address_hexadecimal_string }
				type="text" 
				placeholder=""
				
				rows="1"
			/>
		</div>
		
		<div style="height: 0.5cm"></div>
		
		<div class="card variant-soft-primary p-4" style="color: inherit">
			<header style="text-align: center; font-size: 1.5em">Amount of Octas</header>
			<div style="height: 0.5cm"></div>
			<p 
				style="text-align: center"
			>The actual amount for the transaction is calculate from the input provided.</p>
			<div style="height: 0.5cm"></div>
			<label class="label">
				<input 
					amount_of_octas
					
					on:input={amount_of_Octas_changed}
					bind:value={ amount_of_Octas }
					
					style="padding: 10px"
					class="input" 
					
					type="number" 
					placeholder="Amount of Octas" 
				/>
			</label>
			<div style="height: 0.5cm"></div>
			<p style="text-align: center">Actual Octas Amount: { parse_with_commas (actual_amount_of_Octas_string) }</p>
		</div>
		
		<div style="height: 0.5cm"></div>
		
		<div 
			class="card variant-soft-primary p-4"
			style="
				color: inherit;
			
				display: flex;
				justify-content: right;
			"
		>
			<button 
				make_this_transaction
				style="margin-top: 10px"
				on:click={ ask_for_Octas }
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Ask for Octas</button>
		</div>
		

		
		
		{#if alert_error_text.length >= 1 }
		<aside class="alert variant-soft-error" style="margin: 10px 0">
			<div class="alert-message">
				<p style="white-space: pre-wrap">{ alert_error_text }</p>
			</div>
		</aside>
		<div style="height: .5cm"></div>
		{/if}
		
		
		
		{#if alert_message.length >= 1 }
		<aside class="alert variant-filled" style="margin: 10px 0">
			<div class="alert-message">
				<p style="white-space: pre-wrap">{ alert_message }</p>
			</div>
		</aside>
		{/if}
		
		{#if transaction_success_message.length >= 1 }
		<aside 	class="alert variant-filled-success" style="margin: 10px 0">
			<div class="alert-message">
				<p 
					transaction_message_success
					style="white-space: pre-wrap">{ transaction_success_message }</p>
			</div>
		</aside>
		{/if}
		
		<div style="height: 0.5cm"></div>

		
		<Code_Wall text={ transaction_object } />
		
		<div style="height: 10cm"></div>
	</div>
</Panel>