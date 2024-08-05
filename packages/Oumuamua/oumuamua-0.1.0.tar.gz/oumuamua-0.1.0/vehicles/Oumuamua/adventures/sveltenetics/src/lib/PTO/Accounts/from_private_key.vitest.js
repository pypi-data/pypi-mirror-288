

import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
import { describe, it, expect } from 'vitest';

import assert from 'assert'
import * as AptosSDK from "@aptos-labs/ts-sdk";	

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

describe ('from_private_key', () => {
	
	it ('1', async () => {
		const { 
			account,
			address_hexadecimal_string,
			public_key_hexadecimal_string 
		} = await Account_from_private_key ({
			private_key_hexadecimal_string: "221E8A39C27416F29FD1C58C1CC1C206DE07FCC8BDA2F9678C792CBC3D1CD82D"
		})
		
		
		console.log ({
			address_hexadecimal_string,
			public_key_hexadecimal_string 
		})
		
		assert.equal (
			address_hexadecimal_string,
			"FD0249C3894380002A3D0A9BFA146A9BF7578165F758ED33BF077CFCA4E1EF8A"
		)
		assert.equal (
			public_key_hexadecimal_string,
			"7AE9C8A7349818C877AA906EBE897CFA69BB7F4BC580999AC14CF2DDDEC98141"
		)
	});

});
