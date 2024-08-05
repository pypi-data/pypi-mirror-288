


import { Octas_string_is_permitted } from './Octas_string_is_permitted'

import { describe, it, expect } from 'vitest';
import assert from 'assert'



describe ('Octas_string_is_permitted', () => {
	it ('9999', () => {
		expect (
			Octas_string_is_permitted ("9999")
		).toBe ("yes");
	});
	it ('1', () => {
		expect (
			Octas_string_is_permitted ("1")
		).toBe ("yes");
	});
	it ('123485792340589712039487120934870923487502983475', () => {
		expect (
			Octas_string_is_permitted ("123485792340589712039487120934870923487502983475")
		).toBe ("yes");
	});
	
	describe ('losses', () => {
		it ('9999.9', () => {
			expect (
				Octas_string_is_permitted ("9999.9")
			).toBe ("no");
		});
		
		it ('size zero string', () => {
			expect (
				Octas_string_is_permitted ("")
			).toBe ("no");
		});
		
		it ('non-string', () => {
			expect (
				Octas_string_is_permitted (0)
			).toBe ("no");
		});
	})
});


