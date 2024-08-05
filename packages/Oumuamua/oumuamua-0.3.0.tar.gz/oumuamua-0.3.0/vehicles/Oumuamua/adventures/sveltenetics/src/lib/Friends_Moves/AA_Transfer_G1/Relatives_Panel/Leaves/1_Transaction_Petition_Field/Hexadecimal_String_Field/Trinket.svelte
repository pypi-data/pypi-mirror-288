


<script>

////
///
//
import { onMount, onDestroy } from 'svelte';
import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
//
import { add_unsigned_transaction } from '../Screenplays/add_unsigned_transaction'
//
//\
//\\

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
		
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});


let hexadecimal_string = ""
const add_UT_hexadecimal_string = async () => {
	try {
		freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception_summary = ""
		freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception = ""
		
		await add_unsigned_transaction ({
			unsigned_transaction_hexadecimal_string: hexadecimal_string,
			freight
		})
		
		freight.Unsigned_Transaction_Fields.hexadecimal.button_text = "Added"
	}
	catch (exception) {
		console.error (exception)
		freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception = exception.message;
		freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception_summary = "That hexadecimal could not be converted into an unsigned transaction object";		
		return;
	}

}


</script>

{#if prepared === "yes"}
<div>
	<div>
		<div style="padding: 5px 0 10px;">
			<header
				style="
					text-align: center;
					font-size: 1.4em;
					padding: .2cm 0;
				"
			>Hexadecimal String</header>
			<p
				style="
					text-align: center;
				"
			>The hexadecimal string of the transaction petition can be pasted here.</p>
			<p
				style="
					text-align: center;
				"
			>Recording a photo of the barcode transaction petition is suggested though.</p>
		</div>
	</div>
	
	<label class="label">
		<textarea 
			UT_hexadecimal_string
		
			bind:value={ hexadecimal_string }
			
			style="padding: 10px"
			class="textarea" 
			rows="4" 
			placeholder="" 
		/>
	</label>
	
	{#if freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception.length >= 1 }
		<aside class="alert variant-filled-error">
			<div class="alert-message">
				<p>{ freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception_summary }</p>
				<p>{ freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception }</p>
			</div>
		</aside>
	{/if}
	
	<div style="text-align: right; margin-top: 10px;">
		<button 
			UT_hexadecimal_string_add_button
		
			disabled={ freight.Unsigned_Transaction_Fields.hexadecimal.button_text != "Add" }
			on:click={ add_UT_hexadecimal_string }
			
			style="padding: 10px 60px"
			type="button" 
			class="btn variant-filled"
		>{ freight.Unsigned_Transaction_Fields.hexadecimal.button_text }</button>
	</div>
</div>
{/if}


