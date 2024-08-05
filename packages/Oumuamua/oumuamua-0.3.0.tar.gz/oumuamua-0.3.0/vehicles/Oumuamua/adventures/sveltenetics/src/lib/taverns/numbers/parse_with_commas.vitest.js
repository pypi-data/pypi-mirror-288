


import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
import { describe, it, expect } from 'vitest';

import assert from 'assert'


describe ('parse_with_commas', () => {
	describe ('integer', () => {
		it ('0 digits', () => {
			expect (
				parse_with_commas (0)
			).toBe ("0");
		});
		
		it ('10 digits', () => {
			expect (
				parse_with_commas (1234567890)
			).toBe ("12345,67890");
		});
		
		it ('11 digits', () => {
			expect (
				parse_with_commas (12345678900)
			).toBe ("1,23456,78900");
		});
	})
	
	describe ('strings', () => {
		it ('0 digits', () => {
			expect (
				parse_with_commas ('0')
			).toBe ("0");
		});
		
		it ('10 digits', () => {
			expect (
				parse_with_commas ('1234567890')
			).toBe ("12345,67890");
		});
		
		it ('11 digits', () => {
			expect (
				parse_with_commas ("12345678900")
			).toBe ("1,23456,78900");
		});
	})
	
	describe ('with orb', () => {
		it ('10 digits', () => {
			expect (
				parse_with_commas ('12345678.90')
			).toBe ("123,45678.90");
		});
		
		it ('10 digits', () => {
			expect (
				parse_with_commas ('12345678.123456789')
			).toBe ("123,45678.12345,6789");
		});
		
		it ('10 digits', () => {
			expect (
				parse_with_commas ('12345678.012345678901234567890')
			).toBe ("123,45678.01234,56789,01234,56789,0");
		});
	})
});
