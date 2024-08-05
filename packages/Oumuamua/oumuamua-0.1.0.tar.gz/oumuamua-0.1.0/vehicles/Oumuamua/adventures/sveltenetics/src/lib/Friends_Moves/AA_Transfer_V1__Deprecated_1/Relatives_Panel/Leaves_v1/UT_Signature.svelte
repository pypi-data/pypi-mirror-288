



<script>

import { sign } from './../Screenplays/sign'
import { fiberize_signed_transaction } from '$lib/PTO/Transaction/Signed/Fiberize'
import Net_Choices from '$lib/PTO/Nets/Choices.svelte'

	

////
///
//
export let unsigned_tx = "";
export let unsigned_tx_hexadecimal_string = ""
//
export let signed_transaction_fiberized = ""
export let signed_transaction_hexadecimal_string = ""
//
export let action__signed_transaction_created = ""
//
//\
//\\

let private_key_hexadecimal_string = ""

let net_path = ""
const on_change = ({ net }) => {
	net_path = net.path;
}

const sign_the_transaction = async () => {
	const {
		signed_transaction,
		signed_transaction_hexadecimal_string: _signed_transaction_hexadecimal_string
	} = await sign ({
		unsigned_tx_hexadecimal_string,
		private_key_hexadecimal_string,
		net_path
	})
	signed_transaction_fiberized = fiberize_signed_transaction ({ signed_transaction })
	signed_transaction_hexadecimal_string = _signed_transaction_hexadecimal_string
	
	action__signed_transaction_created ({
		signed_transaction_hexadecimal_string,
		signed_transaction_fiberized
	})
	
	console.log ({ 
		signed_transaction_hexadecimal_string, 
		signed_transaction_fiberized 
	})
}

let message = 'The transaction is not signed.'

</script>



{#if typeof unsigned_tx === "string" }
<div
	style="
		padding: 50px
	"
>
	<p>A barcode picture needs to be scanned to show the sign the transaction.</p>
</div>
{:else}
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
		>Unsigned Transaction Signature Form</header>
		<p>The "Sign" button makes a signature of the unsigned transaction with the private key.</p>
		
		
		<div class="table-container">
			<table class="table table-hover">
				<tbody>
					<tr>
						<td>
							<span style="font-size: 1.5em;">Private Key</span>
							<textarea 
								from_aptos_address
								class="textarea"
								style="min-height: 50px; padding: 10px"
								bind:value={ private_key_hexadecimal_string }
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
				on:click={ sign_the_transaction }
				type="button" 
				class="btn variant-filled"
				style="padding-right: 64px; padding-left: 64px;"
				disabled={ signed_transaction_hexadecimal_string.length >= 1 }
			>{ signed_transaction_hexadecimal_string.length === 0 ? "Sign" : "Signed" }</button>
		</div>
		
		<div>
			{#if signed_transaction_fiberized.length === 0 }
			<aside class="alert">
				<div class="alert-message">
					<p>The transaction is not signed.</p>
				</div>
			</aside>
			{:else}
			<p
				style="
					padding: 20px 0;
				"
			>This is the object likeness of the signed transaction.  The barcode likeness of this object is in the "ST barcode" panel.</p>
			<pre
				class="bg-surface-50-900-token"
				style="
					box-sizing: border-box;
					height: 100%; 
					font-size: 1em;
					white-space: break-spaces;
					word-wrap: break-word;
					text-align: left;
					border-radius: 6px;
				"
			>
{ signed_transaction_fiberized }
			</pre>
			{/if}
		</div>
	</div>
</div>
{/if}