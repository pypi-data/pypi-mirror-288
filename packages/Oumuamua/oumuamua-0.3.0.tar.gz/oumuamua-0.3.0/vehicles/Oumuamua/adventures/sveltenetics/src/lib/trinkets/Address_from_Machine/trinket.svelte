


<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import { 
	Account,
	AccountAddress,
	SigningSchemeInput
} from "@aptos-labs/ts-sdk";


let address_hexadecimal_string = ""
let public_key_hexadecimal_string = ""
let private_key_hexadecimal_string = ""

const generate_address = async () => {
	const account = Account.generate({
		scheme: SigningSchemeInput.Ed25519,
		legacy: false,
	});
	
	address_hexadecimal_string = string_from_Uint8Array (account.accountAddress.data)
	public_key_hexadecimal_string = string_from_Uint8Array (account.publicKey.publicKey.key.data) 
	private_key_hexadecimal_string = string_from_Uint8Array (account.privateKey.signingKey.data)
	
	
	console.log ({ account })
}

</script>


<div style="width: 100%">
	<Panel>
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm',
				'width': '100%'
			})}"
		>Would you like to ask the machine to choose an address?</header>
		
		<div
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'right',
				'font-size': '2em',
				'width': '100%'
			})}"
		>
			<button 
				on:click={ generate_address }
				style="margin-top: 10px"
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Please choose an address for me</button>
		</div>

		<div class="table-container">
			<table class="table table-hover"
				style="background: none"
			>
				<tbody>
					<tr>
						<td>Address</td>
						<td>{ address_hexadecimal_string }</td>
					</tr>
					<tr>
						<td>Public Key</td>
						<td>{ public_key_hexadecimal_string }</td>
					</tr>
					<tr>
						<td>Private Key</td>
						<td>{ private_key_hexadecimal_string }</td>
					</tr>
				</tbody>
				
			</table>
		</div>

	</Panel>
</div>





