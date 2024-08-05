



//	This accepts the aptos SDK signed_transaction object.

/*
	import { fiberize_signed_transaction } from '$lib/PTO/Transaction/Signed/Fiberize'
	const transaction_signature_fiberized = fiberize_signed_transaction ({ signed_transaction })
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

export const fiberize_signed_transaction = ({ 
	signed_transaction 
}) => {
	return JSON.stringify (signed_transaction, replaces, 4);
}