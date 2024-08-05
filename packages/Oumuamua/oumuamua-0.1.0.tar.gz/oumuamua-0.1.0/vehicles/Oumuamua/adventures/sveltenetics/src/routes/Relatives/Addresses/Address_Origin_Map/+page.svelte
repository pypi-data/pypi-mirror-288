



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
import Address_from_Keyboard from '$lib/trinkets/Address_from_Keyboard/Trinket.svelte'
import Address_from_Private_Key from '$lib/trinkets/Address_from_Private_Key/Trinket.svelte'
import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
//
//
//
//\\


let seed_input_as_is;

const elyptic_keyy = elyptic_keyy_prefab ({
	seed_input_element: seed_input_as_is
})

// export let data;

const style_1 = parse_styles ({
	// border: "4px solid black",
	"border-radius": "4px",
	"margin": "10px 0",
	"padding": "10px 20px",
	
	background: 'white',
})

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



let directory_name = "Aptos EEC 25519 Keys"

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


let seed_changes = "mods"
let tabSet = 0;

let possible_waves = parse_with_commas ("100000000000000000000000000000000000000000000000000000000000000000000000000000")


</script>

<style>
	span {
		display: block;
	}
</style>

<svelte:head>
	<title>Address Origin Map</title>
</svelte:head>

<div se--choose-an-address>
	<Panel>
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm'
			})}"
		>Address Origin Map</header>
		<p
			style="
				text-align: center;
				padding: 0 0 1cm;
			"
		>Private Keys are essentially the origin of Addresses on the blockchain.</p>
		<p>
	</Panel>

	<div style="height: 20px"></div>

	<Panel>
		<header
			style="{parse_styles ({
				'display': 'block',
				'text-align': 'center',
				'font-size': '2em',
				'padding': '1cm',
			})}"
		>Abstract</header>
		<p
			style="
				padding: .5cm;
				word-wrap: break-word;
			"
		>
			<span>Addresses on the blockchain can't necessarily be claimed or owned.</span>
			<br />
			<span>It's perhaps like choosing a path that takes you to a region of existence.</span>
			<span>Someone else could possibly choose that same exact path.</span>
			<br />
			<span>Mathematically speaking though, it's very unlikely that someone else coincidentally chooses the same path.</span>
			<br />
			<span style="word-break: break-word">There are 2^256 possible Edward's Elliptic 25519 Keys.</span>
			<span>That's 1.157920892373162e+77 combinations, or greater than { possible_waves } possibilities.</span>
			<br />
			<span>Also, calculating a private key from an address and or public key is probably very tough.</span>
			<br />
			<span>However, if someone does somehow also choose the path that you choose, then they might feel like that the region at the end of the path is theirs to do with as they please.</span>
			
		</p>
	</Panel>
	
	<div style="height: 20px"></div>
	
	<Panel>
		<TabGroup>
			<Tab bind:group={tabSet} name="tab1" value={0}>
				<span>From Keyboard Private Key</span>
			</Tab>
			<Tab bind:group={tabSet} name="tab2" value={1}>
				<span 
					from-private-key--tab
				>From Private Key Hexadecimal</span>
			</Tab>
			<svelte:fragment slot="panel">
				{#if tabSet === 0}
					<Address_from_Keyboard />
				{:else if tabSet === 1}
					<Address_from_Private_Key />
				{/if}
			</svelte:fragment>
		</TabGroup>
	</Panel>
	
	<div style="height: 400px"></div>
	
</div>