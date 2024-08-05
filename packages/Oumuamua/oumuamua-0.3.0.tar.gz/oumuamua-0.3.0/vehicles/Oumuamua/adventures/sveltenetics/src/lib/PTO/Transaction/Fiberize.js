

//	This accepts the aptos SDK unsigned transaction object.

/*
	import { fiberize_transaction } from '$lib/PTO/Transaction/Fiberize'
	const transaction_fiberized = fiberize_transaction ({ transaction })
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

export const fiberize_transaction = ({ transaction }) => {
	return JSON.stringify (transaction, replaces, 4);
}