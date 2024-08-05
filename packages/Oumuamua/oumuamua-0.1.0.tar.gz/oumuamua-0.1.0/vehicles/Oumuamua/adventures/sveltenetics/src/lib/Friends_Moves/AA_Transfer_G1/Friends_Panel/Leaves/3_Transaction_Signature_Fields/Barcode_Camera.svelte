

<script>
///
//
import { ConicGradient } from '@skeletonlabs/skeleton';
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { verify_signature } from './verify_signature'

//
//\

import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck 
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	prepared = "yes"

	open_camera ()
});
onDestroy (() => {
	
});



/*
	

*/
let scanned = "no"
const on_barcode_found = async (decodedText, decodedResult) => {
	console.log ('barcode found!')
	if (scanned === "no") {
		scanned = "yes"
	}
	else {
		return
	}
	
	freight.transaction_signature.hexadecimal_string = decodedText	
	const transaction_signature_Aptos_object = AptosSDK.AccountAuthenticator.deserialize (
		new AptosSDK.Deserializer (
			Uint8Array_from_string (
				freight.transaction_signature.hexadecimal_string
			)
		)
	);
	freight.transaction_signature.Aptos_object = transaction_signature_Aptos_object
	freight.transaction_signature.Aptos_object_fiberized = transaction_signature_Aptos_object
	
	verify_signature ({ freight })
}

const on_scan_error = () => {
	// console.log ('on_error')
}

const open_camera = () => {
	let scanned = "no"
	
	Html5Qrcode.getCameras ().then (devices => {
		console.log ({ devices })
		
		if (devices && devices.length) {
		var cameraId = devices[0].id;
		// .. use this to start scanning.
		}
	}).catch (err => {
		console.error (err)
	});

	
	let html5_QR_barcode_scanner = new Html5QrcodeScanner (
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
	
	html5_QR_barcode_scanner.render (
		on_barcode_found, 
		on_scan_error
	);
}



</script>

<div>
	<div
		style="
			text-align: center;
			padding: .2cm 0;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 1.5em;
				padding: .2cm 0;
			"
		>QR Barcode Camera</header>
		<p>
			<span>After signing the transaction at </span>
			<a 
				target="_blank"
				href="/relatives/signatures"
			>
				/relatives/signatures
			</a>
		</p>
		<p>a picture of the signed transaction QR barcode can be recorded here.</p>
		
		<div style="height: 8px"></div>
		
	</div>

	<div 
		id='reader'
		style="height: 400px; width: 100%; max-width: 600px; margin: 0 auto"
	></div>
</div>