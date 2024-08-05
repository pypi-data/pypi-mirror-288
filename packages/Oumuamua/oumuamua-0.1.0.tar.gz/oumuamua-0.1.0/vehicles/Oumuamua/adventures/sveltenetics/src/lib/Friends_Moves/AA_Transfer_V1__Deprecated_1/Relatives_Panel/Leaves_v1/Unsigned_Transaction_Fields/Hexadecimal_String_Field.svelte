


<script>

import { onMount, onDestroy } from 'svelte';
import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'

//
export let action__add_UT_hexadecimal_string;
//

let button_text = "Add"
let can_add = true;

onMount (() => {
	
})


let unsigned_transaction_hexadecimal_string = ""
let textarea_exception = ""
let textarea_exception_summary = ""
const add_UT_hexadecimal_string = () => {
	console.log ("add_UT_hexadecimal_string", { 
		unsigned_transaction_hexadecimal_string 
	})
	
	textarea_exception = ""	
	textarea_exception_summary = ""
	
	let unsigned_tx = ""
	let unsigned_tx_stringified = ""
	try {
		const {
			unsigned_tx: _unsigned_tx,
			unsigned_tx_stringified: _unsigned_tx_stringified
		} = build_unsigned_tx_from_hexadecimal_string ({
			unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string
		})
		
		unsigned_tx = _unsigned_tx;
		unsigned_tx_stringified = _unsigned_tx_stringified
	}
	catch (exception) {
		console.error (exception)
		textarea_exception = exception;
		textarea_exception_summary = "That hexadecimal could not be converted into an unsigned transaction object";		
		return;
	}
	
	button_text = "Added"
	can_add = false;
	
	action__add_UT_hexadecimal_string ({
		unsigned_tx,
		unsigned_tx_stringified,
		unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string
	})
}


</script>


<div>
	<div>
		<div style="padding: 5px 0 10px;">
			<header
				style="
					text-align: center;
					font-size: 1.4em;
					padding: .2cm 0;
				"
			>Unsigned Transaction Hexadecimal String</header>
			<p
				style="
					text-align: center;
				"
			>The hexadecimal string of the unsigned transaction can be pasted here instead of scanning the barcode of the unsigned transaction.</p>
			<p
				style="
					text-align: center;
				"
			>Recording a photo of the barcode unsigned transaction is suggested though.</p>
		</div>
	</div>
	
	<label class="label">
		<textarea 
			bind:value={ unsigned_transaction_hexadecimal_string }
			health="UT_Barcode_Camera__unsigned_transaction_hexadecimal_string"
			style="padding: 10px"
			class="textarea" 
			rows="4" 
			placeholder="" 
		/>
	</label>
	
	{#if textarea_exception }
		<aside class="alert variant-filled-error">
			<div class="alert-message">
				<p>{ textarea_exception_summary }</p>
				<p>{ textarea_exception }</p>
			</div>
		</aside>
	{/if}
	
	<div style="text-align: right; margin-top: 10px;">
		<button 
			disabled={ can_add != true }
			on:click={ add_UT_hexadecimal_string }
			style="padding: 10px 60px"
			type="button" 
			class="btn variant-filled"
		>{ button_text }</button>
	</div>
</div>