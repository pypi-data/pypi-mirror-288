

<script lang="ts">



///
//
import Navigator from "$lib/trinkets/Navigator/Trinket.svelte";
import Footer from "$lib/trinkets/Footer/Trinket.svelte";

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { onMount, onDestroy, beforeUpdate } from 'svelte'
import { page } from '$app/stores';
import { fade } from 'svelte/transition';
//
import { initializeStores, Modal, Toast } from '@skeletonlabs/skeleton';
import { storePopup } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { Drawer, getDrawerStore } from '@skeletonlabs/skeleton';
import { setInitialClassState, autoModeWatcher } from '@skeletonlabs/skeleton';
import { LightSwitch } from '@skeletonlabs/skeleton';
//
import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
//
import Bug from 'lucide-svelte/icons/bug'
//
//
//\
//\\

///
//
import "../app.css";
//
//\



import {
	lease_roomies_truck,
	give_back_roomies_truck
} from '$lib/Roomies/Trucks'

storePopup.set ({ computePosition, autoUpdate, offset, shift, flip, arrow });			
initializeStores ();


const drawerStore = getDrawerStore();

let roomies_truck_leased = "no"
onMount (async () => {
	autoModeWatcher ();
	setInitialClassState ()
	
	lease_roomies_truck ()
	roomies_truck_leased = "yes"

	//
	// these are for devel purposes
	//
	//
	window.AptosSDK = AptosSDK;
	window.string_from_Uint8Array = string_from_Uint8Array;
	window.Uint8Array_from_string = Uint8Array_from_string;
})

onDestroy (async () => {
	give_back_roomies_truck ()
	roomies_truck_leased = "no"
})

let updated = "no"; 
let built = "no"
beforeUpdate (async () => {
	if (updated === "no") {
		updated = "yes"
		built = "yes"
	}
});



</script>



{#if 
	built === "yes" && 
	roomies_truck_leased === "yes"
}
	<div 
		in:fade={{ duration: 500 }} 
		class="app"
		style="
			display: flex;
			flex-direction: column;
			min-height: 100vh;
		"
	>	
		<div
			style="
				display: flex;
				flex-direction: column;
				min-height: 100%;
			"
		>
			<Modal />
			<Toast />
			<Drawer />
			
			<Navigator />
			
			<main style="min-height: 100vh">
				<slot></slot>
			</main>
			
			<hr class="!border-t-8 !border-double" />
			
			<Footer />
		</div>
	</div>
{/if}


<style>

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}

	footer {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		padding: 12px;
	}
	
	@media (min-width: 480px) {
		footer {
			padding: 12px 0;
		}
	}
</style>