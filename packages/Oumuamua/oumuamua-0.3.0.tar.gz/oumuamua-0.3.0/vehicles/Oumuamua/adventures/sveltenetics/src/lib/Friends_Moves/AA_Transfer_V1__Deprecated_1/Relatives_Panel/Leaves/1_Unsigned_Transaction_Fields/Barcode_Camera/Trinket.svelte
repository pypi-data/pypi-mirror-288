

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

import { add_unsigned_transaction } from '../Screenplays/add_unsigned_transaction'

import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
//
//\




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


const on_camera_success = async (decodedText, decodedResult) => {
	console.log ('A barcode was found!')
	if (freight.Unsigned_Transaction_Fields.camera.searching === "yes") {
		freight.Unsigned_Transaction_Fields.camera.searching = "no"
	}
	else {
		return
	}
	
	await add_unsigned_transaction ({
		unsigned_transaction_hexadecimal_string: decodedText,
		freight
	})
	
	freight.Unsigned_Transaction_Fields.camera.barcode_found = "yes"
	freight.Unsigned_Transaction_Fields.info_text = "The barcode was scanned and the unsigned transaction object built."
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
			>The "Request Camera Permissions" button opens the barcode scan.</p>
			<p
				style="
					text-align: center;
				"
			>If there's a problem with the scan, maybe try refreshing the browser and checking if the camera is connected and on.</p>
		</div>
	</div>

	<div 
		id='reader'
		style="height: 400px; width: 100%; max-width: 600px; margin: 0 auto"
	></div>
</div>
