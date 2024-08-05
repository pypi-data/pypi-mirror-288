
/*
import { ask_APT_count } from '$lib/PTO/APT/Count'
const APT_count_ask = await ask_APT_count ({ 
	address_hexadecimal_string,
	net_path
})
if (APT_count_ask.effective !== "yes") {
	// APT_count_ask.exception
	
	return;
}
 
Octa_count = APT_count_ask.Octa_count;
*/

import { Aptos, AptosConfig, AccountAddress, Network } from "@aptos-labs/ts-sdk";
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import Fraction from 'fraction.js';

import { furnish_string } from 'procedures/furnish/string'


export const ask_APT_count = async ({
	address_hexadecimal_string,
	net_path
}) => {
	console.info ({ net_path })
	
	var resource = `0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>`

	// const proceeds = await fetch (`${ net_path }/accounts/${ address_hexadecimal_string }/resources`)
	const proceeds = await fetch (
		`${ net_path }/accounts/${ address_hexadecimal_string }/resource/${ resource }`
	)
	/*const proceeds = await fetch (
		`${ net_path }/accounts/${ address_hexadecimal_string }`
	)*/
	const status = proceeds.status;
	
	if (status === 404) {
		const enhanced = await proceeds.json ()
		const error_code = furnish_string (enhanced, [ 'error_code' ], '');
		const message = furnish_string (enhanced, [ 'message' ], '');
		
		let exception = ""
		if (error_code === "resource_not_found") {
			exception = `${ error_code }\n\n${ message}\n\nThis might be an address that has 0 transactions associated with it.`;
		}
		else {
			exception = `${ error_code }: ${ message}`
		}
		
		return {
			error_code,
			effective: "no",
			exception
		}
	}
	if (status === 400) {
		return {
			effective: "no",
			exception: await proceeds.text (),
			error_code: ""
		}
	}
	if (status === 200) {
		const enhanced = await proceeds.json ()
		const Octa_count = enhanced.data.coin.value;

		return {
			effective: "yes",
			exception: "",
			error_code: "",
			
			Octa_count
		}
	}
	
	return {
		effective: "no",
		exception: "An exception occurred.",
		error_code: ""
	}
}



