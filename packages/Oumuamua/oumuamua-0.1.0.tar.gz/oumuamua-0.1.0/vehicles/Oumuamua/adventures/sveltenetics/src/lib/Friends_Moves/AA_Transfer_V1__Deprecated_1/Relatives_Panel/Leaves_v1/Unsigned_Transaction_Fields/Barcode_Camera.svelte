

<script>

///
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
//
import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
//
//\

////
///
export let unsigned_transaction_hexadecimal_string;
//
export let action__add_UT_hexadecimal_string;
//\
//\\

let barcode_found = "no"
let camera_is_searching = "no"

let message = "Waiting for unsigned transaction."
if (barcode_found === "yes") {
	message = "The unsigned transaction was added."
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
	
	action__add_UT_hexadecimal_string ({
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
	<div>
		<div style="padding: 5px 0 10px;">
			<header
				style="
					text-align: center;
					font-size: 1.4em;
					padding: .2cm 0;
				"
			>QR Barcode Camera</header>
			<p
				style="
					text-align: center;
				"
			>A picture of the unsigned transaction QR barcode can be recorded here.</p>
		</div>
	</div>

	<div 
		id='reader'
		style="height: 400px; width: 100%; max-width: 600px; margin: 0 auto"
	></div>
</div>
