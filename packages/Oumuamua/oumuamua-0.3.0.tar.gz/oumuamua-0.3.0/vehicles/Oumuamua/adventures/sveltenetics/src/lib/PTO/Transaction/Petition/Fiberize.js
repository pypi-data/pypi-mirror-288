

/*
import { 
	fiberize_transaction_petition_object,
	fiberize_transaction_petition_bytes
} from '$lib/PTO/Transaction/Petition/Fiberize'
*/

/*
	import { 
		fiberize_transaction_petition_object,
	} from '$lib/PTO/Transaction/Petition/Fiberize'
	const transaction_petition_fiberized = fiberize_transaction_petition_object ({
		transaction_petition_object
	})
*/

/*
	import { 
		fiberize_transaction_petition_bytes 
	} from '$lib/PTO/Transaction/Petition/Fiberize'
	const transaction_petition_fiberized = fiberize_transaction_petition_bytes ({
		transaction_petition_bytes
	})
*/

import * as Aptos_SDK from "@aptos-labs/ts-sdk";

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'

const replaces = (key, value) => {
	// console.log ("replaces:", key, value)
	
	if (typeof value === 'bigint') {
		return value.toString ();
	}
	if (value instanceof Uint8Array) {
		return string_from_Uint8Array (value)
	}
	
	return value;
}


export const fiberize_transaction_petition_object = ({
	transaction_petition_object
}) => {
	return JSON.stringify (transaction_petition_object, replacerWithPath (), 4);
}


export const fiberize_transaction_petition_bytes = ({
	transaction_petition_bytes
}) => {
	const deserialized = new Aptos_SDK.Deserializer (transaction_petition_bytes);
	const transaction_petition_object = Aptos_SDK.SimpleTransaction.deserialize (deserialized);
	return JSON.stringify (transaction_petition_object, replacerWithPath (), 4);
}

