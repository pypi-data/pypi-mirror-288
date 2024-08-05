




////
//
import { sign } from './sign'
//
import { describe, it, expect } from 'vitest';
import assert from 'assert'
//
//\\

function areUint8ArraysEqual (arr1, arr2) {
	if (arr1.length !== arr2.length) {
		return "nuh";
	}

	for (let i = 0; i < arr1.length; i++) {
		if (arr1[i] !== arr2[i]) {
			return "nuh";
		}
	}

	return "yuh";
}

describe ('sign', () => {
	it ('1', async () => {
		const unsigned_tx_hexadecimal_string = ""
		const private_key_hexadecimal_string = ""
		
		const { signed_tx_hexadecimal_string } = await sign ({
			unsigned_tx_hexadecimal_string,
			private_key_hexadecimal_string
		})
	});
});
