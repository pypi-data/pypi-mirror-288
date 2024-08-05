

// "src/lib/PTO/Transaction/Petition/Logistics.vitest.js"

import _isEqual from 'lodash/isEqual'

import { unpack, pack } from './Logistics'

import { describe, it, expect } from 'vitest';
import assert from 'assert'

describe ("Logistics", () => {
	it.skip ("transforms 1", () => {
		const transaction_petition_1 = {
			"rawTransaction": {}
		}
		
		const proceeds = pack ({ bracket: transaction_petition_1 })
		const equality = _isEqual (
			proceeds,
			{
				"proceeds": {
					"rawTransaction": {}
				},
				"fluctuations": []
			}
		) 
		if (equality !== true) {
			console.error (proceeds)
			throw new Error ("not equal.")
		}
	})
	
	it ("transforms 2", () => {
		const transaction_petition_1 = {
			"10": {
				"20": {
					"40": 6n
				},
				"30": 5n,
				"70": new Uint8Array ([ 0, 0, 12 ])
			}
		}
		
		const a_pack = pack ({ bracket: transaction_petition_1 })
		const unpacked = unpack ({ a_pack })
		
		const equality = _isEqual (
			transaction_petition_1,
			unpacked
		) 
		if (equality !== true) {
			console.error ({
				transaction_petition_1,
				unpacked
			})
			throw new Error ("not equal.")
		}
	})
	
	it ("transforms 3", () => {
		const transaction_petition_1 = {
			"10": [
				{
					"data": new Uint8Array ([ 0, 0, 0, 0 ]),
				},
				{
					"value": 100000000n
				}
			]
		}
		
		const a_pack = pack ({ bracket: transaction_petition_1 })
		const unpacked = unpack ({ a_pack })
		
		const equality = _isEqual (
			transaction_petition_1,
			unpacked
		) 
		if (equality !== true) {
			console.error ({
				transaction_petition_1,
				unpacked
			})
			throw new Error ("not equal.")
		}
	})
	
	it ("transforms 4", () => {
		const transaction_petition_1 = {
			"rawTransaction": {
				"sender": {
					"data": new Uint8Array ([ 0, 0, 0, 0 ])
					// "data": "522D906C609A3D23B90F072AD0DC74BF857FB002E211B852CE38AD6761D4C8FD"
				},
				
				//"sequence_number": "5",
				"sequence_number": 5n,
				
				
				"payload": {
					"entryFunction": {
						"module_name": {
							"address": {
								"data": new  Uint8Array ([ 0, 0, 0, 0 ]),
								// "data": "0000000000000000000000000000000000000000000000000000000000000001"
							},
							"name": {
								"identifier": "aptos_account"
							}
						},
						"function_name": {
							"identifier": "transfer"
						},
						"type_args": [],
						"args": [
							{
								"data": new Uint8Array ([ 0, 0, 0, 0 ]),
								// "data": "26F4F8D7C5526BA7DA453041D3A858CFEA06D911C90C2E40EDA2A7261826858C"
							},
							{
								"value": 100000000n
								// "value": "00E1F50500000000"
							}
						]
					}
				},
				"max_gas_amount": 200000n,
				"gas_unit_price": 100n,
				"expiration_timestamp_secs": 1722470518n,
				"chain_id": {
					"chainId": 145
				}
			}
		}
		
		const a_pack = pack ({ bracket: transaction_petition_1 })
		const unpacked = unpack ({ a_pack })
		
		const equality = _isEqual (
			transaction_petition_1,
			unpacked
		) 
		if (equality !== true) {
			console.dir ({
				transaction_petition_1,
				unpacked
			}, {
				depth: 10
			})
			throw new Error ("not equal.")
		}
	})
})