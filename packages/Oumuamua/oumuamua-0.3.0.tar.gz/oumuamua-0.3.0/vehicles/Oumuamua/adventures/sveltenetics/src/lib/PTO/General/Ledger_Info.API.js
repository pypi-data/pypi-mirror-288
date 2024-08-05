
// https://aptos.dev/en/build/apis/fullnode-rest-api-reference#tag/general/get/

/*
	import { request_ledger_info } from '$lib/PTO/General/Ledger_Info.API'
	const { enhanced } = await request_ledger_info ({ net_path })
	const { chain_id } = enhanced;
*/


const ask = async (URL, {
	method = "GET",
	timeout = Number.POSITIVE_INFINITY
}) => {
	return await new Promise ((resolve, reject) => {
		var xhr = new XMLHttpRequest();
		xhr.open (method, URL, true);
		xhr.timeout = timeout

		xhr.onload = function () {
			if (xhr.status === 200) {
				resolve ({
					status: xhr.status,
					object: JSON.parse (xhr.responseText)
				});
				return;
			} 

			reject ("The ask failed with status:", xhr.status)
		};
		xhr.onerror = function () {
			reject ("The ask failed.")
		};
		xhr.ontimeout = function () {
			reject ("The ask timed out.")
		};

		xhr.send ();
	})

}

export const request_ledger_info = async ({ net_path }) => {
	const proceeds = await ask (net_path, {
		timeout: 1000
	})
	const enhanced = proceeds.object;
	
	// console.info (proceeds)
	
	// const proceeds = await fetch (net_path);
	// console.log (proceeds.status)

	if (proceeds.status === 404) {

	}
	
	// const enhanced = await proceeds.json ()
	
	return {
		enhanced
	};
}