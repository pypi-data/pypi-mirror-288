


<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { Account_from_private_key } from '$lib/PTO/Accounts/from_private_key'
	
import { clipboard } from '@skeletonlabs/skeleton';

import { 
	AccountAddress
} from "@aptos-labs/ts-sdk";

let private_key_hexadecimal_string_input = ""

let private_key_hexadecimal_string = ""
let public_key_hexadecimal_string = ""
let address_hexadecimal_string = ""
let exception = ""

import { save_keys } from '$lib/taverns/keys_directory/save'
	
let directory_name = "Aptos Pouch 1"

const calculate_address = async () => {
	try {
		const { 
			account,
			address_hexadecimal_string: address_hexadecimal_string_1,
			public_key_hexadecimal_string: public_key_hexadecimal_string_1
		} = await Account_from_private_key ({
			private_key_hexadecimal_string: private_key_hexadecimal_string_input
		})
		
		public_key_hexadecimal_string = public_key_hexadecimal_string_1
		address_hexadecimal_string = address_hexadecimal_string_1
		private_key_hexadecimal_string = private_key_hexadecimal_string_input
		
		exception = ""
	}
	catch (exception_) {
		console.error (exception_)
		exception = exception_.message
		address_hexadecimal_string = ""
		public_key_hexadecimal_string = ""
	}
}

const save = async () => {
	save_keys ({
		directory_name,
		hexadecimal_public_key: public_key_hexadecimal_string,
		hexadecimal_address: address_hexadecimal_string,
		hexadecimal_private_key: private_key_hexadecimal_string
	})
}

</script>


<div style="width: 100%">
	<Panel>
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm 0 .4cm',
				'width': '100%'
			})}"
		>Address from Private Key</header>
		<p
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '1em',
				'word-break': 'break-word',
				'width': '100%'
			})}"
		>Example: 889ABCFED89736504127603417265389FAEDBC8F9EDABCFEB014276354526135</p>

		<div 
			style="width: 100%; background: none; margin-top: 10px"
		>
			<div 
				class="input-group-shim"
				style="width: 150px"
			>Private Key</div>
			<textarea 
				from-private-key--private-key-hexadecimal
				bind:value={ private_key_hexadecimal_string_input }
				class="textarea" 
				rows="4" 
				placeholder="" 
				style="background: none; padding: .3cm; position: relative; width: 100%"
			/>
		</div>
		
		<div
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'right',
				'font-size': '2em',
				'width': '100%'
			})}"
		>
			<button 
				from-private-key--calculate
				on:click={ calculate_address }
				style="margin-top: 10px"
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Calculate</button>
		</div>
		
		{#if exception.length >= 1}
		<aside class="alert variant-filled" style="margin: 10px 0">
			<div class="alert-message">
				<p>{ exception }</p>
			</div>
		</aside>
		{/if}
		
		<div class="table-container">
			<table class="table table-hover"
				style="background: none"
			>
				<tbody>
					<tr>
						<td style="width: 30%">Private Key</td>
						<td style="width: 50%"
							from-private-key--private_key_hexadecimal_string
						>{ private_key_hexadecimal_string }</td>
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={private_key_hexadecimal_string}
							>Copy</button>
						</td>
					</tr>
					<tr>
						<td style="width: 30%">Address</td>
						<td style="width: 50%"
							from-private-key--address_hexadecimal_string
						>{ address_hexadecimal_string }</td>
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={address_hexadecimal_string}
							>Copy</button>
						</td>
					</tr>
					<tr>
						<td style="width: 30%">Public Key</td>
						<td style="width: 50%"
							from-private-key--public_key_hexadecimal_string
						>{ public_key_hexadecimal_string }</td>
						<td style="width: 20%">
							<button 
								type="button" 
								class="btn bg-gradient-to-br variant-gradient-primary-secondary"
								use:clipboard={public_key_hexadecimal_string}
							>Copy</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</Panel>
	
	<div 
		class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
		style="background: none;"
	>
		<div class="input-group-shim">Directory Name</div>
		<input 
			bind:value={ directory_name }
			type="search" 
			placeholder="" 
			style="text-indent: 10px; padding: 15px 5px; background: none; border-radius: 4px"
		/>
		<div>
			<button 
				on:click={ save }
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Save as Directory</button>
		</div>
	</div>
</div>





