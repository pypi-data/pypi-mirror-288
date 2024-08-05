
// "src/lib/taverns/hexadecimal/Uint8Array_from_string.vitest.js"

import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
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

describe ('Uint8Array_from_string', () => {
	describe ('no goal', () => {
		it ('0011GG', () => {
			expect (() => {
				Uint8Array_from_string ("0011GG")
			}).toThrow (`The nibbles at indexes 4 & 5 did not convert into a byte integer.`)
		});
		
		it ('0011F', () => {
			expect (() => {
				Uint8Array_from_string ("0011F")
			}).toThrow (`The hexadecimal string "0011F" does not divide by 2.`)
		});
	})
	
	it ('00000000', () => {
		expect (areUint8ArraysEqual (
			Uint8Array_from_string ("00000000"), 
			Uint8Array.from ([ 0, 0, 0, 0 ])
		)).toBe ("yuh");
	})
	
	it ('0011FF', () => {
		expect (areUint8ArraysEqual (
			Uint8Array_from_string ("0011FF"), 
			Uint8Array.from ([ 0, 17, 255 ])
		)).toBe ("yuh");
	});
	
	it ('EFFE', () => {
		expect (areUint8ArraysEqual (
			Uint8Array_from_string ("EFFE"), 
			Uint8Array.from ([ 239, 254 ])
		)).toBe ("yuh");
	});
	
	it ('FF', () => {
		expect (areUint8ArraysEqual (
			Uint8Array_from_string ("FF"), 
			Uint8Array.from ([ 255 ])
		)).toBe ("yuh");
	});
});
