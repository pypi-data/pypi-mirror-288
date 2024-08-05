

/*
	
*/


import { 
	Aptos, Account, AccountAddress,
	AptosConfig, Network, SigningSchemeInput } from "@aptos-labs/ts-sdk";
	
import * as AptosSDK from "@aptos-labs/ts-sdk";	

import { ed25519 } from '@noble/curves/ed25519';

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import { hexadecimalize } from './screenplays/hexadecimalize'




import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
	


export const elyptic_keyy_prefab = () => {
	return (() => {
		let trinket = ""
		
		const controls = {
			public_key_hexadecimal_string: "",
			
			//
			// this is the private key
			//
			//
			private_key_choosen: "no",
			seed_hexadecimal: "",
			seed_hexadecimal_show: "",
			seed_hexadecimal_choosen: "no",
			
			// size in nibbles
			nibble_count: 64,
			
			at_change: [],
			changed (action) {
				trinket.at_change.push (action)
			},
			
			say_changed () {
				for (let E = 0; E < trinket.at_change.length; E++) {
					trinket.at_change [E] ({ trinket })
				}
			},			
			
			showbiz () {
				trinket = this;
				console.log ({ trinket })
			},

			async generate_keys () {
				const { 
					account,
					address_hexadecimal_string,
					public_key_hexadecimal_string 
				} = await Account_from_private_key ({
					private_key_hexadecimal_string: "89ABCDEF89AB8EFD9ACB76051243760512437568C9AFEBDC89FAEDBC07615234"
				});
				
				console.log ({
					account,
					address_hexadecimal_string,
					public_key_hexadecimal_string 
				});
			},

			async on_key_up (event) {
				if (event.isComposing || event.keyCflavor === 229) {
					return;
				}
				
				
				// const seed_crate = trinket.$refs.seed;
				// const seed_hex_count_crate = trinket.$refs.seed_hex_count;
				// const build_showy_key_button = trinket.$refs.build_showy_key_button;
				
				var ctrl_key = event.ctrlKey;
				var shift_key = event.shiftKey;
				var meta_key = event.metaKey;
				var event_key = event.key;
				
				console.log ("event_key:", event_key)
				
				const original = event.target.value;
				
				const { 
					hexadecimal, 
					score, 
					note, 
					choosen, 
					private_key_choosen, 
					hexadecimal_public_key,
					hexadecimal_address
				} = await hexadecimalize ({
					original,
					nibble_count: trinket.nibble_count
				});
				
				trinket.seed_hexadecimal = hexadecimal
				trinket.seed_hexadecimal_show = note
				trinket.seed_hexadecimal_choosen = choosen
				trinket.private_key_choosen = private_key_choosen
				trinket.hexadecimal_public_key = hexadecimal_public_key
				trinket.hexadecimal_address = hexadecimal_address
				
				trinket.say_changed ()
			}
		}
		
		controls.showbiz ()
		
		controls.generate_keys ()
		
		return controls;
	}) ()
}