

/*
const {
	private_key_choosen,
	score,
	note,
	
	hexadecimal_private_key,
	hexadecimal_public_key,
	hexadecimal_address
} = hexadecimalize ({
	original: "SGOWYTKDHGUFIDOSYGLEYTIFJDSLGYOWOTLDHSDFGORUDKOSYWHGJJHOFIEEYFKT",
	nibble_count: 64
})
*/

import { ed25519 } from '@noble/curves/ed25519';
import { 
	Aptos, Account, AccountAddress,
	AptosConfig, Network, SigningSchemeInput 
} from "@aptos-labs/ts-sdk";


import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
	

const cyfi = {
	"W": "0",
	"E": "1",
	"R": "2",
	"T": "3",
	
	"Y": "4",
	"U": "5",
	"I": "6",
	"O": "7",
	
	"S": "8",
	"D": "9",
	"F": "A",
	"G": "B",
	
	"H": "C",
	"J": "D",
	"K": "E",
	"L": "F"
}

//	
//	
//	
//	
const produce_keys = async ({ hexadecimal_private_key }) => {
	// const private_key_uint_8_array = Uint8Array_from_string (hexadecimal_private_key)
	// const public_key_uint_8_array = await ed25519.getPublicKey (private_key_uint_8_array);
	// const public_key_hexadecimal_string = string_from_Uint8Array (public_key_uint_8_array)
	// return public_key_hexadecimal_string
	
	const { 
		account,
		address_hexadecimal_string,
		public_key_hexadecimal_string 
	} = await Account_from_private_key ({
		private_key_hexadecimal_string: hexadecimal_private_key
	})
	
	return {
		address_hexadecimal_string,
		public_key_hexadecimal_string
	}
}

//	
//	This converts the keyboard characters into hexadecimals
//	according the cyfi.
//	
export const hexadecimalize = async ({
	original,
	nibble_count
}) => {
	let hexadecimal_private_key = ""
	
	for (let E = 0; E < original.length; E++) {
		const character = original [E].toUpperCase ();
		
		if (typeof cyfi [ character ] != "string") {
			return {
				choosen: "no",
				
				score: "no",
				note: `Character ${ character } at ${ E + 1 } is not valid.`,
				
				hexadecimal_private_key
			}
		}
		
		if (hexadecimal_private_key.length >= nibble_count) {
			return {
				choosen: "no",
				
				score: "no",
				note: `There are ${ original.length - nibble_count } more nibbles than the limit size of ${ nibble_count }`,
				
				hexadecimal_private_key
			}
		}
		
		hexadecimal_private_key += cyfi [ character ];
	}
	
	var public_key_hexadecimal_string = ""
	var address_hexadecimal_string = ""
	if (hexadecimal_private_key.length == nibble_count) {
		var { 
			public_key_hexadecimal_string, 
			address_hexadecimal_string 
		} = await produce_keys ({
			hexadecimal_private_key
		})
	}
	
	return {
		private_key_choosen: hexadecimal_private_key.length == nibble_count ? "yes" : "no",
		
		score: "yes",
		note: `${ hexadecimal_private_key.length } of ${ nibble_count } characters choosen`,
		
		// deprecated
		hexadecimal: hexadecimal_private_key,
		
		hexadecimal_private_key,
		hexadecimal_public_key: public_key_hexadecimal_string,
		hexadecimal_address: address_hexadecimal_string
	};
}