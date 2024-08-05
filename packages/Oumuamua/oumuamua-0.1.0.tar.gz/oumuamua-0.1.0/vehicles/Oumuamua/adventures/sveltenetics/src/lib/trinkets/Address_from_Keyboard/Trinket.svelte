
<script>

////
//
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";
import { writable } from 'svelte/store';
//
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
import { elyptic_keyy_prefab } from '$lib/trinkets/elyptic_keyy'
//
//
import { make_trends } from './screenplays/trends'
import { save_keys } from '$lib/taverns/keys_directory/save'
//
//\\


let seed_input_as_is;

const elyptic_keyy = elyptic_keyy_prefab ({
	seed_input_element: seed_input_as_is
})

// export let data;



const choose_button_trends = {
	border: "4px solid black",
	"border-radius": "4px",
	"margin": "10px 0",
	"padding": "5px",
	
	"min-width": "150px",
	
	// "box-shadow": '0 0 0 2px white, 0 0 0 4px black',
	
	"text-decoration": "solid line-through",
	"cursor": "initial"
}

let trends = make_trends ()


let directory_name = "Aptos Pouch 1"

let hexadecimal_public_key = ""
let hexadecimal_address = ""

let seed_hexadecimal = "";
let seed_hexadecimal_show = elyptic_keyy.seed_hexadecimal_show;
let seed_hexadecimal_choosen = ""
elyptic_keyy.changed (({ trinket }) => {
	console.log ('changed:', trinket)
	
	seed_hexadecimal = trinket.seed_hexadecimal;
	seed_hexadecimal_show = trinket.seed_hexadecimal_show;
	seed_hexadecimal_choosen = trinket.seed_hexadecimal_choosen;
	
	if (trinket.private_key_choosen === "yes") {
		hexadecimal_public_key = trinket.hexadecimal_public_key
		hexadecimal_address = trinket.hexadecimal_address
		
		choose_button_trends ["text-decoration"] = "initial"
		choose_button_trends ["cursor"] = "pointer"
	}
	else {
		hexadecimal_public_key = ""
		hexadecimal_address = ""
		
		choose_button_trends ["text-decoration"] = "solid line-through"
		choose_button_trends ["cursor"] = "initial"
	}
})

function save () {		
	if (hexadecimal_address.length >= 1) {
		save_keys ({
			directory_name,
			hexadecimal_public_key,
			hexadecimal_address,
			hexadecimal_private_key: seed_hexadecimal
		})
	}
}

let seed_changes = "mods"
let tabSet = 0;
	


</script>

<div>
	<p>To choose the seed hexadecimal number, please click on the input below, and use the characters:</p>
	<p>WERT YUIO</p>
	<p>SDFG HJKL</p>

	<p>Those characters are then changed into hexadecimals in this group:</p>
	<p>0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F</p>

	<textarea
		se--from-keyboard-private-key-textarea
		on:keyup={ elyptic_keyy.on_key_up }
		bind:this={ seed_input_as_is }
		style="{ trends.textarea }"
	/>
	
	<div
		style="{ trends.action }"
	>
		<span
			style="{ trends.decal }"
		>
			<p style="font-weight: bold">hexadecimal private key</p>
		</span> 
		<span 
			se--private-key-hexadecimal
			style="{ trends.hexadecimal_seed }"
		>
			{ seed_hexadecimal }
		</span>
	</div>
	
	<div
		style="{ trends.action }"
	>
		<span
			style="{ trends.decal }"
		>
			<p style="font-weight: bold">hexadecimal public key</p>
			<p>This is made once the private key is choosen.</p> 
		</span>
		<span 
			se--public-key-hexadecimal
			style="{ trends.hexadecimal_seed }">
			{ hexadecimal_public_key }
		</span>
	</div>
	
	<div
		style="{ trends.action }"
	>
		<span
			style="{ trends.decal }"
		>
			<p style="font-weight: bold">hexadecimal address</p>
			<p>This is made once the private key is choosen.</p> 
			<p>APT can be received at this address.</p> 				
		</span>
		<span 
			se--address-hexadecimal
			style="{ trends.hexadecimal_seed }"
		>
			{ hexadecimal_address }
		</span>
	</div>
	
	<div
		style="{ trends.action }"
	>
		<span
			style="{ trends.decal }"
		>
			<p style="font-weight: bold">note</p>
		</span> 
		<span>{ seed_hexadecimal_show }</span>
	</div>
	
	<div
		style="{parse_styles ({
			"display": 'flex',
			"justify-content": "right"
		})}"
	>	
		<div
			style="{parse_styles ({
				"display": 'flex',
				"justify-content": "space-around"
			})}"
		>
			<input
				bind:value={ directory_name }
				style="{ trends.textarea }"
				type="text" 
			/>
					
			<div style="width: 10px"></div>
			
			<button 
				on:click={ save }
				style="{ parse_styles (choose_button_trends) }"
			>
				save as folder
			</button>
		</div>
	</div>
</div>