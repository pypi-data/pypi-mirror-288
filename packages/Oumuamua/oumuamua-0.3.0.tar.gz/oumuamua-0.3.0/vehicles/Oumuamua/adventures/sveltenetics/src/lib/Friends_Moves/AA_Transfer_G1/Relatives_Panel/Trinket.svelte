

<script>


/*
	import AA_Transfer_G1_Relatives_Panel from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Trinket.svelte'
*/

////
///
import { getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
//
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
//
//
import UT_Fields from './Leaves/1_Transaction_Petition_Field/Trinket.svelte';
import Unsigned_Transaction_Trinket from './Leaves/2_Transaction_Petition/Trinket.svelte';
import Unsigned_Transaction_Signature_Trinket from './Leaves/3_Transaction_Signature_Field/Trinket.svelte';
import Transaction_Signature_Trinket from './Leaves/4_Transaction_Signature/Trinket.svelte'
//
//
import Unfinished from './Trinkets/Unfinished.svelte'
//
import { ConicGradient } from '@skeletonlabs/skeleton';
//
//\
//\\


////
///
//	props
//
export let modal_store;
//
//\
//\\



import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land,
	destroy_truck
} from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Logistics/Truck'

let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	refresh_truck ()
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	verify_land ()
	calculate_next_button_text ()
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
		calculate_next_button_text ()
	})
	
	prepared = "yes"
});
onDestroy (() => {
	destroy_truck ()
});

let current_tab = 1;



const close_the_modal = () => {
	modal_store.close ();
}


let next_button_text = "Next";
let calculate_next_button_text = () => {
	if (freight.current.next === "yes") {
		next_button_text = "Next"
	}
	else if (freight.current.next === "no, last") {
		next_button_text = "Last"
	}
	else {
		next_button_text = "Unfinished"
	}
}

let panel_text = "Panel 1 of 4"
const write_panel_text = () => {
	panel_text = `Panel ${ current_tab } of 4`
}

let go_back = () => {
	if (freight.current.back === "yes") {
		current_tab -= 1
		write_panel_text ()
	}
}
let go_next = () => {
	// check if can go on
	if (freight.current.next === "yes") {
		current_tab += 1
		write_panel_text ()
	}
	else {
		freight.unfinished_extravaganza.showing = "yes"
	}
}

</script>

{#if $modal_store [0] && prepared === "yes" }
<div 
	style="
		position: relative;
		top: 0;
		left: 0;
		padding: 0;
		width: 100vw;
		height: calc(100vh - 36px);
		
		overflow: hidden;
	"
>
	<div
		class="bg-surface-50-900-token border border-primary-500/30"
		style="
			display: flex;
			
			position: absolute;
			top: 10px;
			left: 10px;
			height: calc(100% - 20px);
			width: calc(100% - 20px);
			border-radius: 8px;
			
			overflow: hidden;
			
			flex-direction: column;
		"
	>
		<div
			style="
				position: absolute;
				top: 0;
				left: 0;
				right: 0;
				bottom: 0;
				width: 100%;
				
				box-sizing: border-box;
				padding: 0 10px 0;
				
				overflow: scroll;
			"
		>
			<div style="height: 2cm" />			
			{#if current_tab === 1}
				<UT_Fields />
			{:else if current_tab === 2}
				<Unsigned_Transaction_Trinket />
			{:else if current_tab === 3}
				<Unsigned_Transaction_Signature_Trinket />
			{:else if current_tab === 4}
				<Transaction_Signature_Trinket />
			{/if}
			<div style="height: 5cm" />
		</div>

		<Unfinished />

		<footer
			class="bg-surface-50-900-token border border-primary-500/30"
			style="
				position: absolute;
				bottom: 0;
				left: 0;
				width: 100%;
				height: 70px;
			"
		>
			<hr class="!border-t-2" />
			
			<div 
				class="modal-footer"
				style="
					display: flex;
					align-items: center;
					justify-content: space-between;
				
					position: absolute;
					bottom: 0;
					left: 0;
					width: 100%;
					padding: 10px;
				"
			>
				<button class="btn variant-filled" on:click={close_the_modal}>
					Quit
				</button>
				
				<div>{ panel_text }</div>
				
				<div style="display: flex">
					<button 
						modal-back
					
						disabled={ freight.current.back != "yes" }
						on:click={ go_back }
						
						class="btn variant-filled"
					>
						Back
					</button>
					<div style="width: 20px"></div>
					<button 
						modal-next
					
						disabled={ next_button_text === "Last" }
						on:click={ go_next }
						
						class="btn variant-filled" 
					>
						{#if next_button_text === "Unfinished" }
						<span>
							<ConicGradient 
								stops={[
									{ color: 'transparent', start: 0, end: 25 },
									{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
								]} 
								spin
								width="w-5"
							/>
						</span>
						{/if}
						<span>
							{ next_button_text }
						</span>
					</button>
				</div>
			</div>
		</footer>
	</div>
</div>
{/if}