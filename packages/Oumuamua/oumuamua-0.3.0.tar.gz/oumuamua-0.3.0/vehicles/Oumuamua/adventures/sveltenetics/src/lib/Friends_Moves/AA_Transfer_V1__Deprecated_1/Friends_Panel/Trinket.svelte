

<script>



////
///
//
import Transaction_Fields_Trinket from './Leaves/1_Transaction_Fields/Trinket.svelte'
import Unsigned_Transaction_Trinket from './Leaves/2_Unsigned_Transaction/Trinket.svelte'
import Transaction_Signature_Fields_Trinket from './Leaves/3_Transaction_Signature_Fields/Trinket.svelte'
import Transaction_Signature_Trinket from './Leaves/4_Transaction_Signature/Trinket.svelte'
import Ask_Consensus from './Leaves/5_Ask_Consensus/Trinket.svelte'
//
import Unfinished from './Trinkets/Unfinished.svelte'
//
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
//
import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land,
	destroy_truck
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
//
import { popup } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
//
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


let panel_text = "Panel 1 of 5"
const write_panel_text = () => {
	panel_text = `Panel ${ current_tab + 1 } of 5`
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



let next_button_text = "";
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

//
let prepared = "no"
let Truck_Monitor;
let freight;
let truck;
onMount (() => {
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

const close_the_modal = () => {
	modal_store.close ();
}


let current_tab = 0;
//
const open_tab_0 = () => {
	current_tab = 0;
}
const open_tab_1 = () => {
	current_tab = 1;
}
const open_tab_2 = () => {
	current_tab = 2;
}
const open_tab_3 = () => {
	current_tab = 3;
}
const open_tab_4 = () => {
	current_tab = 4;
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
				display: flex;
				justify-content: center;
				flex-direction: column;
			"
		>
			<header
				style="
					padding: 0.2cm 0;
					text-align: center;
					font-size: 1.2em;
				"
			>Transfer</header>
			<hr class="!border-t-2" />
		</div>
	
		<div
			style="
				position: relative;
				top: 0;
				left: 0;
				width: 100%;
				height: calc(100% - 70px);
				
				overflow: scroll;
			"
		>
			<nav
				style="
					position: sticky;
					top: 0;
					left: 0;
					width: 100%;
				"
			></nav>
			
			{#if prepared === "yes"}
			<main
				style="
					position: relatives;
					top: 0;
					left: 0;
					right: 0;
					bottom: 0;
					
					width: 100%;
					height: 100%;
					
					box-sizing: border-box;
					padding: 0 10px 0;
					
					overflow: scroll;
				"
			>
				<div style="height: 1cm" />
				{#if current_tab === 0}
					<Transaction_Fields_Trinket />
				{:else if current_tab === 1}
					<Unsigned_Transaction_Trinket />
				{:else if current_tab === 2}
					<Transaction_Signature_Fields_Trinket />
				{:else if current_tab === 3}
					<Transaction_Signature_Trinket />
				{:else if current_tab === 4}
					<Ask_Consensus />
				{/if}
				
				<div style="height: 5cm" />
			</main>
			{/if}
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
						class="btn variant-filled"
						on:click={go_back}
					>
						Back
					</button>
					<div style="width: 20px"></div>
					<button 
						modal-next
						disabled={ next_button_text === "Last" }
						class="btn variant-filled" 
						on:click={go_next}
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