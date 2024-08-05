



<script>

import { sign } from './sign'
import { fiberize_signed_transaction } from '$lib/PTO/Transaction/Signed/Fiberize'
import Net_Choices from '$lib/PTO/Nets/Choices.svelte'
import { onMount, onDestroy } from 'svelte';
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 

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
	
	freight.current.land = "Unsigned_Transaction_Signature"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});

let private_key_hexadecimal_string = ""


const sign_the_transaction = async () => {
	freight.Unsigned_Transaction_Signature.private_key_hexadecimal_string = private_key_hexadecimal_string
	
	const {
		signed_transaction,
		signed_transaction_hexadecimal_string
	} = await sign ({
		unsigned_tx_hexadecimal_string: freight.Unsigned_Transaction_Fields.hexadecimal_string,
		private_key_hexadecimal_string
	})
	
	freight.Unsigned_Transaction_Signature.Aptos_object_fiberized = fiberize_signed_transaction ({ signed_transaction })
	freight.Unsigned_Transaction_Signature.hexadecimal_string = signed_transaction_hexadecimal_string
	
	freight.Unsigned_Transaction_Signature.signed = "yes"
}


</script>



{#if prepared === "yes"}
<div>
	<div
		style="
			text-align: center;
			padding: 0 1cm 1cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: 1cm 0;
			"
		>Transaction Signature Field</header>
		<p>The "Sign" button creates a <b>signature</b> from the <b>transaction petition</b> with the <b>private key.</b></p>
		
		<div class="table-container">
			<table class="table table-hover">
				<tbody>
					<tr>
						<td>
							<span style="font-size: 1.5em;">Private Key</span>
							<textarea 
								private_key
							
								bind:value={ private_key_hexadecimal_string }

								
								class="textarea"
								style="min-height: 50px; padding: 10px"
								type="text" 
								placeholder=""
							/>
						</td>
					</tr>
				</tbody>
			</table>
		</div>		
		
		<div
			style="margin: 10px 0; text-align: right"
		>
			<button 
				sign
			
				on:click={ sign_the_transaction }
				disabled={ freight.Unsigned_Transaction_Signature.hexadecimal_string.length >= 1 }

				type="button" 
				class="btn variant-filled"
				style="padding-right: 64px; padding-left: 64px;"
			>{ freight.Unsigned_Transaction_Signature.hexadecimal_string.length === 0 ? "Sign" : "Signed" }</button>
		</div>
	</div>
</div>
{/if}