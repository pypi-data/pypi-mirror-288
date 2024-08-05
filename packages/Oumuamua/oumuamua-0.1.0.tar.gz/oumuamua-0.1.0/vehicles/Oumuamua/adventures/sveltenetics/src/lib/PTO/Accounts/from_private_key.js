
/*
	import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
	const { 
		account,
		address_hexadecimal_string,
		public_key_hexadecimal_string 
	} = await Account_from_private_key ({
		private_key_hexadecimal_string: "89ABCDEF89AB8EFD9ACB76051243760512437568C9AFEBDC89FAEDBC07615234"
	})
	
	console.info ({ account })
*/


import { 
	Aptos, 
	Account, 
	AccountAddress,
	AptosConfig, 
	Network, 
	SigningSchemeInput 
} from "@aptos-labs/ts-sdk";
	
import * as AptosSDK from "@aptos-labs/ts-sdk";	

import { ed25519 } from '@noble/curves/ed25519';

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

export const Account_from_private_key = async ({
	private_key_hexadecimal_string
}) => {
	/*
	const private_key_uint_8_array = Uint8Array_from_string (private_key_hexadecimal_string)
	const account = Account.fromPrivateKey ({ 
		privateKey: new AptosSDK.Ed25519PrivateKey (private_key_uint_8_array)
	});
	
	const public_key = account.publicKey;
	// const public_key_hexadecimal_string = account.publicKey.toString ()
	const public_key_hexadecimal_string = string_from_Uint8Array (public_key.key.data);
	
	
	const address = account.accountAddress;
	const address_hexadecimal_string = string_from_Uint8Array (address.data);
	// const address_hexadecimal_string = account.accountAddress.toString ();
	*/
	
	const account = AptosSDK.Account.fromPrivateKey ({ 
		privateKey: new AptosSDK.Ed25519PrivateKey (
			Uint8Array_from_string (private_key_hexadecimal_string)
		), 
		legacy: false 
	});
	
	const address = account.accountAddress;
	const address_hexadecimal_string = string_from_Uint8Array (account.accountAddress.data);
	
	const public_key = account.publicKey.publicKey;
	
	console.log ({ account, public_key })
	
	const public_key_hexadecimal_string = string_from_Uint8Array (public_key.key.data);
	
	console.log (
		"equal private keys:", 
		account.privateKey.toString ()
	)
	
	
	/*console.log ({
		account,
		
		public_key: string_from_Uint8Array (public_key.key.data),
		address: string_from_Uint8Array (address.data),
		
		address_hexadecimal_string,
		public_key_hexadecimal_string
	})*/
	
	return {
		account,
		
		public_key,
		public_key_hexadecimal_string,
		
		address,
		address_hexadecimal_string
	}
}