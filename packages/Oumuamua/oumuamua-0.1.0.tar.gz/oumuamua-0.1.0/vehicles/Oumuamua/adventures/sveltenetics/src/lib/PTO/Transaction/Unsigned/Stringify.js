

//
//	Caution: Deprecated 
//
//	Fresh Version is: "Transaction/Petition/Fiberize"
//


//	This accepts the aptos SDK unsigned transaction object.

/*
	import { stringify_UT } from '$lib/PTO/Transaction/Unsigned/Stringify'
	const unsigned_transaction_fiberized = stringify_UT ({ unsigned_tx })
*/

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'

const replaces = (key, value) => {
	if (typeof value === 'bigint') {
		return value.toString ();
	}
	
	if (value instanceof Uint8Array) {
		return string_from_Uint8Array (value)
	}
	
	return value;
}

export const stringify_UT = ({ unsigned_tx }) => {
	return JSON.stringify (unsigned_tx, replaces, 4);
}