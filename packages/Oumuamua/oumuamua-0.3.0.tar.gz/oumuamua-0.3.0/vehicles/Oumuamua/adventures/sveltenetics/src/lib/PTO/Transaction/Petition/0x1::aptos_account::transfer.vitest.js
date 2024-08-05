

// "lib/PTO/Transaction/Petition/0x1::aptos_account::transfer.vitest.js"

		
import * as Aptos_SDK from "@aptos-labs/ts-sdk";

import { ask_for_accounts } from '$lib/PTO/Accounts/Examples'
import { send_coins_from_faucet } from '$lib/PTO/Faucet/send'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
	
import { unpack, pack } from './Logistics'

import { 
	build_transaction_petition_object_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Petition/object_from_hexadecimal_string'

import { 
	fiberize_transaction_petition_object,
	fiberize_transaction_petition_bytes
} from '$lib/PTO/Transaction/Petition/Fiberize'
		
	
import { describe, it, expect } from 'vitest';
import assert from 'assert'

const pick_expiration = ({
	after_seconds
}) => {
	const after_seconds_ = parseInt (after_seconds);
	const expireTimestamp = new Aptos_SDK.U64 (Math.floor (Date.now () / 1000) + after_seconds_).value;
	
	// console.log ("exp:", expireTimestamp)
	// console.log ("now:", Math.floor (Date.now () / 1000))
	
	return expireTimestamp
}

describe ("Transation Petition", () => {
	describe ("0x1::aptos_account::transfer", () => {
		it ("Can be reversed", async () => {
			const account_1 = ask_for_accounts () ["1"]
			const account_2 = ask_for_accounts () ["2"]
			const account_3 = Aptos_SDK.Account.generate ();
			
			
			const account_1_address = Aptos_SDK.AccountAddress.from (
				Uint8Array_from_string (account_1 ["address"])
			);
			const account_2_address = Aptos_SDK.AccountAddress.from (
				Uint8Array_from_string (account_2 ["address"])
			);
			const account_3_address = account_3.accountAddress
			
			const account_1_private_key = account_1 ["private key"]
			const account_1_public_key = Uint8Array_from_string (account_1 ["public key"])
			
			
			const net_path = "https://api.devnet.aptoslabs.com/v1"
			const transfer_amount = 1e7;
						
			
			
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
			
			/*
			const aptos = new Aptos_SDK.Aptos (new Aptos_SDK.AptosConfig ({		
				fullnode: net_path,
				network: Aptos_SDK.Network.CUSTOM
			}));
			*/
			
			/*
				1. transaction_petition_object
				2. transaction_petition_as_bytes
				3. transaction_petition_hexadecimal_string
				
				4. transaction_petition_as_bytes_reversal
				5. transaction_petition_object_reversal
				
				----
				1. transaction_petition_object
				2. transaction_petition_fiberized
			 */
			
			const aptos = new Aptos_SDK.Aptos (new Aptos_SDK.AptosConfig ({}));
		
			
			
			/*
				[{
					data: new Uint8Array ([ 0, 0, 255 ])
				},{
					value: 1000000n
				}]
			*/
			
			/*
			const functionArguments = [{
				data: new Uint8Array ([ 0, 0, 255 ])
			},{
				value: 1000000n
			}]
			*/
			
			var functionArguments = [
				account_2_address, 
				new Aptos_SDK.U64 (1e8)
			]
			
			/*var functionArguments = [
				"0x123", 
				1_000_000
			]*/
			
			console.log ({
				functionArguments
			})

			const options = {}
			const transaction_petition_object = await aptos.transaction.build.simple ({
				sender: account_1_address,
				data: {
					function: "0x1::aptos_account::transfer",
					// typeArguments: [],
					
					// functionArguments?
					functionArguments
				},
				options
			});
			
			const a_pack = pack ({ bracket: transaction_petition_object })
			const unpacked = unpack ({ a_pack })
			
			/*const unsigned_transaction_Aptos_object = AptosSDK.SimpleTransaction.deserialize (
				new AptosSDK.Deserializer (
					Uint8Array_from_string (unsigned_tx_hexadecimal_string)
				)
			);*/
			
			const expireTimestamp = pick_expiration ({ 
				after_seconds: 600 
			})
			
			/*
				const raw_transaction = new Aptos_SDK.RawTransaction (
					from_address,
					BigInt (sequenceNumber),
					payload,
					
					BigInt(maxGasAmount),
					BigInt(gasUnitPrice),
					BigInt(expireTimestamp),
					new ChainId (chainId),
				);
			*/
			
			const sequenceNumber = transaction_petition_object ["rawTransaction"] ["sequence_number"]
			const payload = transaction_petition_object ["rawTransaction"] ["payload"]
			const raw_transaction_object = new Aptos_SDK.RawTransaction (
				account_1_address,
				BigInt (sequenceNumber),
				payload,
				
				BigInt (200000),
				BigInt (100),
				BigInt (expireTimestamp),
				new Aptos_SDK.ChainId (145),
			);
			
			console.log ({
				unpacked,
				raw_transaction_object,
				transaction_petition_object
			})
			
			const account_1_aptos = Aptos_SDK.Account.fromPrivateKey ({ 
				privateKey: new Aptos_SDK.Ed25519PrivateKey (
					Uint8Array_from_string (account_1_private_key)
				), 
				legacy: false 
			});
			
			const signature = aptos.transaction.sign ({ 
				signer: account_1_aptos, 
				transaction: raw_transaction_object
			});
			
			const committed_transaction = await aptos.transaction.submit.simple ({ 
				transaction: raw_transaction_object, 
				senderAuthenticator: signature
			});
				
			console.log ({ committed_transaction, unpacked })
			
			/*
			const senderAuthenticator = aptos.transaction.sign({
				signer: sender,
				transaction: unpacked
			});
			 */
			return;
			
			/*
			const [userTransactionResponse] = await aptos.transaction.simulate.simple({
				signerPublicKey: account_1_public_key,
				transaction_petition_object
			});
			console.log(userTransactionResponse)
			*/
			
			const transaction_petition_fiberized = fiberize_transaction_petition_object ({
				transaction_petition_object
			})
			
			/*
			const raw_transaction_bytes = transaction_petition_object.rawTransaction.bcsToBytes ()
			const raw_transaction_deserializer = new Aptos_SDK.Deserializer (raw_transaction_bytes);
			const raw_transaction = Aptos_SDK.RawTransaction.deserialize (raw_transaction_deserializer);
			const raw_transaction_fiberized = fiberize_transaction_petition_object ({
				transaction_petition_object: raw_transaction
			})
			console.log ({
				raw_transaction_bytes,
				raw_transaction_deserializer,
				raw_transaction,
				raw_transaction_fiberized
			})
			*/
			
			
			const transaction_petition_as_bytes = transaction_petition_object.bcsToBytes ()
			const transaction_petition_as_hex = transaction_petition_object.bcsToHex ()
			
			console.info ({
				transaction_petition_as_hex
			})
			
			
			
			
			
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
				transaction_petition_object,
				
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