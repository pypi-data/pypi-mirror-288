



// "lib/PTO/Transaction/Petition/Petition.vitest.js"

		
import * as Aptos_SDK from "@aptos-labs/ts-sdk";

import { ask_for_accounts } from '$lib/PTO/Accounts/Examples'
import { send_coins_from_faucet } from '$lib/PTO/Faucet/send'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
	

import { 
	build_transaction_petition_object_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Petition/object_from_hexadecimal_string'

import { 
	fiberize_transaction_petition_object,
	fiberize_transaction_petition_bytes
} from '$lib/PTO/Transaction/Petition/Fiberize'
		
	
import { describe, it, expect } from 'vitest';
import assert from 'assert'

describe ("Transation Petition", () => {
	describe.skip ("0x1::coin::transfer", () => {
		it ("Can be reversed", async () => {
			const account_1 = ask_for_accounts () ["1"]
			const account_2 = ask_for_accounts () ["2"]
			
			const account_3 = Aptos_SDK.Account.generate ();
			
			const the_function = "0x1::coin::transfer"
			const net_path = "https://api.devnet.aptoslabs.com/v1"
			const transfer_amount = 1e7;
						
			const account_1_address = Aptos_SDK.AccountAddress.from (
				Uint8Array_from_string (account_1 ["address"])
			);
			const account_2_address = Aptos_SDK.AccountAddress.from (
				Uint8Array_from_string (account_2 ["address"])
			);
			const account_3_address = account_3.accountAddress
			
			console.log ({ 
				account_1_address,
				account_3_address
			})

			
			const net_path_faucet = "https://faucet.devnet.aptoslabs.com/mint"			
			const { tx } = send_coins_from_faucet ({
				amount: 1e8,
				address: account_3_address,
				URL: net_path_faucet
			})
			
			const aptos = new Aptos_SDK.Aptos (new Aptos_SDK.AptosConfig ({		
				fullnode: net_path,
				network: Aptos_SDK.Network.CUSTOM
			}));

			const options = {}
			const transaction_petition_object = await aptos.transaction.build.simple ({
				sender: account_1_address,
				data: {
					function: "0x1::coin::transfer",
					typeArguments: ["0x1::aptos_coin::AptosCoin"],
					functionArguments: [
						account_2_address,
						transfer_amount
					]
				},
				options
			});
			const transaction_petition_fiberized = fiberize_transaction_petition_object ({
				transaction_petition_object
			})
			const transaction_petition_as_bytes = transaction_petition_object.bcsToBytes ()
			const transaction_petition_hexadecimal_string = string_from_Uint8Array (transaction_petition_as_bytes)

	
			const {
				transaction_petition_object: reversal__transaction_petition_object,
				transaction_petition_fiberized: reversal__transaction_petition_fiberized
			} = build_transaction_petition_object_from_hexadecimal_string ({
				transaction_petition_hexadecimal_string
			})
			
			assert.equal (
				transaction_petition_hexadecimal_string,
				string_from_Uint8Array (reversal__transaction_petition_object.bcsToBytes ())
			)
			
			console.info ({
				deserialized: Aptos_SDK.SimpleTransaction.deserialize (
					new Aptos_SDK.Deserializer (
						transaction_petition_object.bcsToBytes ()
					)
				).rawTransaction.payload.entryFunction.args,
				
				transaction_petition_fiberized,
				reversal__transaction_petition_fiberized
			})
		})
	})
})