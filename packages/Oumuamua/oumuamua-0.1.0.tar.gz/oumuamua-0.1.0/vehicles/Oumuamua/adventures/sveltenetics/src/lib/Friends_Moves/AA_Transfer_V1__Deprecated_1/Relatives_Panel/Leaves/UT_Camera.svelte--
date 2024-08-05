

<script>

///
//
import { getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
import { getToastStore } from '@skeletonlabs/skeleton';			
//
import { 
	parse_styles 
} from '$lib/trinkets/styles/parse.js';
import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
//
//\

////
///
export let unsigned_transaction_hexadecimal_string;
export let barcode_found;
//
export let unsigned_transaction_scanned;
//\
//\\

const toastStore = getToastStore();

let camera_is_searching = "no"

let message = "Waiting for unsigned transaction."
if (barcode_found === "yes") {
	message = "The unsigned transaction was added."
}


let unsigned_transaction_hexadecimal_string_from_textarea = ""
let UT_hexadecimal_string_from_textarea_exception = ""
let UT_hexadecimal_string_from_textarea_exception_summary = ""
const add_UT_hexadecimal_string = () => {
	console.log ("add_UT_hexadecimal_string", { 
		unsigned_transaction_hexadecimal_string_from_textarea 
	})
	
	unsigned_transaction_hexadecimal_string = unsigned_transaction_hexadecimal_string_from_textarea
	camera_is_searching = "yes"
	
	UT_hexadecimal_string_from_textarea_exception = ""	
	UT_hexadecimal_string_from_textarea_exception_summary = ""
	
	let unsigned_tx = ""
	let unsigned_tx_stringified = ""
	try {
		const {
			unsigned_tx: _unsigned_tx,
			unsigned_tx_stringified: _unsigned_tx_stringified
		} = build_unsigned_tx_from_hexadecimal_string ({
			unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string_from_textarea
		})
		
		unsigned_tx = _unsigned_tx;
		unsigned_tx_stringified = _unsigned_tx_stringified
	}
	catch (exception) {
		console.error (exception)
		UT_hexadecimal_string_from_textarea_exception = exception;
		UT_hexadecimal_string_from_textarea_exception_summary = "That hexadecimal could not be converted into an unsigned transaction object";		
	}
	
	message = "The unsigned transaction was added."
	
	unsigned_transaction_scanned ({
		unsigned_tx,
		unsigned_tx_stringified,
		unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string_from_textarea
	})
}

const on_camera_success = async (decodedText, decodedResult) => {
	console.log ('on_success!')
	if (camera_is_searching === "no") {
		camera_is_searching = "yes"
	}
	else {
		return
	}
	
	unsigned_transaction_hexadecimal_string = decodedText
	
	const {
		unsigned_tx,
		unsigned_tx_stringified
	} = build_unsigned_tx_from_hexadecimal_string ({
		unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string
	})
	
	unsigned_transaction_scanned ({
		unsigned_tx,
		unsigned_tx_stringified,
		unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string
	})
	
	message = "The barcode was scanned and the unsigned transaction object built."
}

const on_camera_error = () => {
	// console.log ('on_error')
}




const open_camera = () => {
	Html5Qrcode.
	getCameras ().
	then (devices => {
		console.log ({ devices })
		
		if (devices && devices.length) {
			var cameraId = devices[0].id;
			// .. use this to start scanning.
		}
	}).
	catch (err => {
		console.error (err)
	});

	
	let HTML5_QR_Barcode_Scanner = new Html5QrcodeScanner (
		"reader", 
		{
			fps: 10,
			qrbox: {
				width: 500, 
				height: 500
			},
			// rememberLastUsedCamera: true,
			// Only support camera scan type.
			// supportedScanTypes: [ Html5QrcodeScanType.SCAN_TYPE_CAMERA ]
		}, 
		/* verbose= */ false
	);
	
	HTML5_QR_Barcode_Scanner.render (
		on_camera_success,
		on_camera_error
	);
}


onMount (() => {
	open_camera ()
})



</script>


<div>
	<div
		style="
			text-align: center;
			padding: 0 0 1cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: 1cm 0;
			"
		>Unsigned Transaction Barcode Camera</header>
		<p>After making an unsigned transaction barcode,</p>
		<p>a picture of the unsigned transaction can be recorded here.</p>
		
		<div style="height: 8px"></div>
		<p>After making the picture, an ask can be sent to the consensus for addition to the blockchain.</p>
	</div>
	

	<aside class="alert variant-filled"
		style="
			display: flex;
			flex-direction: row;
			margin: 12px auto;
			max-width: 500px;
		"
	>
		<div>
			{#if barcode_found !== "yes"}
			<ConicGradient 
				stops={[
					{ color: 'transparent', start: 0, end: 25 },
					{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
				]} 
				spin
				width="w-5"
			/>
			{/if}
		</div>
		<p
			style="
				margin: 0;
				padding-left: 12px;
			"
		>{message}</p>
	</aside>
	
	<div 
		id='reader'
		style="height: 400px; width: 100%; max-width: 600px; margin: 0 auto"
	></div>
	
	<hr class="!border-t-8" style="margin: 50px 0" />
	
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
		
		<label class="label">
			<textarea 
				bind:value={ unsigned_transaction_hexadecimal_string_from_textarea }
				health="UT_Barcode_Camera__unsigned_transaction_hexadecimal_string"
				style="padding: 10px"
				class="textarea" 
				rows="4" 
				placeholder="" 
			/>
		</label>
		
		
		{#if UT_hexadecimal_string_from_textarea_exception}
			<aside class="alert variant-filled-error">
				<div class="alert-message">
					<p>{ UT_hexadecimal_string_from_textarea_exception_summary }</p>
					<p>{UT_hexadecimal_string_from_textarea_exception}</p>
				</div>
			</aside>
		{/if}
					
		
		<div style="text-align: right; margin-top: 10px;">
			<button 
				on:click={ add_UT_hexadecimal_string }
				style="padding: 10px 60px"
				type="button" 
				class="btn variant-filled"
			>Add</button>
		</div>
	</div>
</div>