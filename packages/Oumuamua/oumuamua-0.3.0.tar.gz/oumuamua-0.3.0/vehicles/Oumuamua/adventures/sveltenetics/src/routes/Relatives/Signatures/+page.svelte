


<script>

////
///
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
import AA_Transfer_G1_Relatives_Panel from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Trinket.svelte'
//
//
import { onMount } from 'svelte'
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
//
//\
//\\



const trends = {
	article: parse_styles ({
		padding: '.3cm',
		// "max-width": "15cm"
		
	}),
	article_header: parse_styles ({
		padding: '.3cm',
		'font-size': '2em',
		"text-align": "center",
	}),
	panel: {
		position: 'relative',
		display: 'inline-flex',
		//'width': '33%', 
		'align-items': 'center',
		'justify-content': 'center',
		'flex-direction': 'column'
	},
}

const modal_store = getModalStore ();
const open_consideration_modal = async () => {
	console.log ('open_consideration_modal')
	
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: AA_Transfer_G1_Relatives_Panel,
			props: { 
				modal_store
			}
		}
	});
}

let barcode_element = ""

let scanning = "yes"
let private_key_hexadecimal_string = ""


let reader;
onMount (() => {

})

</script>

<svelte:head>
	<title>Signatures</title>
</svelte:head>


<div>
	<div class="card text-column"
		style="
			display: block;
			height: auto;
			padding: 1cm 0 1cm;
		"
	>
		<h1>Signatures</h1>

		<div style="height: 1cm"></div>

		<p
			style="text-align: center"
		>Signatures are the consent necessary for the consensus to save a transaction to the blockchain.</p> 
		
		<div style="height: 0.5cm"></div>
		
		<p
			style="text-align: center"
		><b>Private Key</b> + <b>Transaction Petition</b> -> <b>Signature</b></p> 
		
		<div style="height: 0.5cm"></div>
		
		
		<p style="text-align: center">
			<b>Transaction Petition</b> + <b>Signature</b> + <b>Consensus Consent</b> -> <b>Blockchain Transaction</b>
		</p>

		<div style="height: .5cm"></div>
	</div>

	
	<div style="height: 1cm"></div>
	
	<section
		style={ parse_styles ({
			position: 'relative',
			display: 'grid',
			'width': '100%',
			'grid-template-columns': 'repeat(auto-fit, minmax(400px, 1fr))',
			'grid-gap': '10px'
		}) }
	>
		<Panel styles={ trends.panel }>			
			<div style="height: 0.5cm"></div>
			<div class="relative inline-block">
				<span class="badge variant-soft-primary absolute -right-0 z-10"
					style="
						display: none;
						left: 50%;
						bottom: -30px;
						transform: translateX(-50%);
					"
				>Version 1</span>
				<button 
					octas_gifts__version_1
					
					on:click={ open_consideration_modal }
					type="button" 
					class="btn bg-gradient-to-br variant-gradient-primary-secondary"
					style="
						font-size: 1.3em;
						padding: 12px 36px;
						margin-top: 10px
					"
				>Aptos Account Transfer</button>
			</div>
			<div style="height: 10px"></div>
			<article style="{ trends.article }">
				<p style="text-align: center">This is for signing an "Aptos Account Transfer" transaction.</p>
			</article>
			<div style="height: 0.5cm"></div>
		</Panel>
	</section>
</div>


