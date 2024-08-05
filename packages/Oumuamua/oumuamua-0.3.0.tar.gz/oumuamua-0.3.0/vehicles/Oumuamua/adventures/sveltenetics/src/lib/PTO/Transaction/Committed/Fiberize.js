

//	This accepts the aptos SDK signed_transaction object.

/*
	import { fiberize_committed_transaction } from '$lib/PTO/Transaction/Committed/Fiberize'
	const committed_transaction_fiberized = fiberize_committed_transaction ({ committed_transaction })
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

export const fiberize_committed_transaction = ({ 
	committed_transaction 
}) => {
	return JSON.stringify (committed_transaction, replaces, 4);
}