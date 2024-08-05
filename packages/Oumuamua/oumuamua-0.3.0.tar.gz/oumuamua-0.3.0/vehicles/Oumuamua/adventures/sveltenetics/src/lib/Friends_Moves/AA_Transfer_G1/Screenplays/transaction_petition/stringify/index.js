




/*
import { 
	fiberize_transaction_petition_object,
	fiberize_transaction_petition_bytes
} from '$lib/PTO/Transaction/Petition/Fiberize'
*/

/*
	import { stringify_TP_AO } from '../stringify'
	const TP_stringified = stringify_TP_AO ({ TP_AO })
*/

/*
	import { stringify_TP_bytes } from '../stringify'
	const TP_stringified = stringify_TP_bytes ({
		TP_bytes
	})
*/

import * as Aptos_SDK from "@aptos-labs/ts-sdk";

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


export const stringify_TP_AO = ({
	TP_AO
}) => {
	return JSON.stringify (TP_AO, replaces, 4);
}


export const stringify_TP_bytes = ({
	TP_bytes
}) => {
	const deserialized = new Aptos_SDK.Deserializer (TP_bytes);
	const TP_AO = Aptos_SDK.SimpleTransaction.deserialize (deserialized);
	return JSON.stringify (TP_AO, replaces, 4);
}

