


import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { describe, it, expect } from 'vitest';

import assert from 'assert'

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

describe ('string_from_Uint8Array', () => {
	describe ('no goal', () => {
		it ('[ 255, 0 ]', () => {
			expect (string_from_Uint8Array (Uint8Array.from ([ 255, 0 ]))).toBe ("FF00");
		});
	})
	
	it ('[ 255 ]', () => {
		expect (string_from_Uint8Array (Uint8Array.from ([ 255 ]))).toBe ("FF");
	});
	
	it ('[ 255, 0 ]', () => {
		expect (string_from_Uint8Array (Uint8Array.from ([ 255, 0 ]))).toBe ("FF00");
	});
});
