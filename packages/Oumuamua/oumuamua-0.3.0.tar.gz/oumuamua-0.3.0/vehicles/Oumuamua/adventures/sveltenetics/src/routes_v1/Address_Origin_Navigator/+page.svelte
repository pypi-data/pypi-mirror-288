


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

<svelte:head>
	<title>Ask Machine for Address</title>
</svelte:head>

<div style="width: 100%">
	<Panel>
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm'
			})}"
		>Address Origin Navigator</header>
	
		<p
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '1em',
				'padding': '0 0 0',
				'width': '100%',
				'margin': '0 auto',
				'max-width': '400px'
			})}"
		>The button below sends an ask to the Address Origin Navigator to choose a private key and find the address at the destination of the path.</p>

		<p
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '1em',
				'padding': '1cm 0',
				'width': '100%'
			})}"
		>Bothering the Navigator might be unwise though.</p>
		
		<div
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'right',
				'font-size': '2em',
				'width': '100%',
				'margin': '1cm 0',
				'text-align': 'center'
			})}"
		>
			<button 
				on:click={ generate_address }
				style="
					margin-top: 10px;
					white-space: break-spaces;
					max-width: 700px;
					font-size: .7em;
					margin: 0 auto;
					border: 4px solid black;
					padding: 28px;
				"
				type="button" 
				class="btn"
			>I beg, please have mercy upon me and show me an address and public key from a private keys.  I am not fit to make decisions and reliquish my decision making priveledges.</button>
		</div>
		
		<div style="height: 2cm"></div>

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
		
		<div style="height: 2cm"></div>
	</Panel>
</div>





