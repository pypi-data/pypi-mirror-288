




// https://aptos.dev/en/build/apis/fullnode-rest-api-reference#tag/general/get/

/*
	import { ask_convert_APT_to_Octas } from '$lib/origin/math/APT_to_Octas.RPC.js'
	const { enhanced, Octas } = await ask_convert_APT_to_Octas ({ APT })
*/

import { ask_for_freight } from '$lib/Roomies/Trucks'

export const ask_convert_APT_to_Octas = async ({ APT }) => {
	const freight = ask_for_freight ();
	
	const proceeds = await fetch (freight.origin_address + "/math/APT_to_Octas",  {
		method: 'PATCH',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify ({
			APT
		})
	});
	const enhanced = await proceeds.json ()
	
	// console.info ({ enhanced })
	
	return {
		enhanced,
		// Octas
	};
}