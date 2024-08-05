




<script>

///
//
import { make_barcode } from '$lib/Barcode/make'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
//
import { onMount, onDestroy } from 'svelte';
//
//\

////
///
export let signed_tx_hexadecimal_string = ""
//\
//\\


let barcode_element = ""


const show_QR_of_signed_tx = ({
	barcode_element
}) => {
	make_barcode ({
		barcode_element,
		hexadecimal_string: signed_tx_hexadecimal_string,
		size: 400
	})
}

onMount (async () => {
	console.log ("ST_Barcode onMount", { signed_tx_hexadecimal_string })
	
	if (signed_tx_hexadecimal_string.length >= 1) {
		show_QR_of_signed_tx ({
			barcode_element,
			signed_tx_hexadecimal_string
		})
	}
});


</script>





{#if signed_tx_hexadecimal_string.length >= 1 }
<div 
	style="
		height: 100%; 
		overflow: scroll;
		padding: .2cm;
	"
>
	<div
		style="
			text-align: center;
			padding: 1cm 0 .3cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .3cm 0;
			"
		>Signed Transaction Barcode</header>
		<p>This is the QR barcode equivalent of the signed transaction from the "ST Object" panel.</p> 
		<p>
			<span>With a picture of this at </span>
			<a 
				target="_blank"
				href="/relatives/friends"
			>
				/relatives/friends
			</a>
			<span>an ask can be sent to the consensus.</span>
		</p>
	</div>
	
	<hr class="!border-t-8" />
	
	<pre
		style="
			display: flex;
			justify-content: center;
		"
	>
		<code id="result" bind:this={barcode_element}></code>
	</pre>
	
	<hr class="!border-t-8" />
	

	
	<div>
		<header
			style="
				text-align: center;
				font-size: 1.4em;
				padding: .2cm 0;
			"
		>The Signature as a Hexadecimal String</header>
		<p
			style="
				text-align: center;
				padding: 0 0 10px;
			"
		>This is the hexadecimal string equivalent of the barcode above.</p>
		
		<p
			health="UT_Object__UT_hexadecimal_string"
			class="bg-surface-50-900-token"
			style="
				box-sizing: border-box;
				height: 100%; 
				font-size: 1em;
				white-space: break-spaces;
				word-wrap: break-word;
				text-align: left;
			"
		>{ signed_tx_hexadecimal_string }</p>
	</div>
	
	<div
		style="height: 200px"
	>
	</div>
</div>
{:else}
<div>
	To make a barcode, the Unsigned Transaction needs to be signed.
</div>
{/if}