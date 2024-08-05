


<script>

/*
import Conference from '$lib/trinkets/Conference/Trinket.svelte'

<Conference 
	prepare={ prepare }
	enhance={ enhance }
>
	<div slot="leaves">
		<Transaction_Fields_Trinket 
			leaf="1" 
		/>
		<Unsigned_Transaction_Trinket 
			leaf="2" 
		/>
		<Transaction_Signature_Fields_Trinket 
			leaf="3" 
		/>
		<Transaction_Signature_Trinket 
			leaf="4"
		/>
		<Ask_Consensus 
			leaf="5"
		/>
	</div>
</Conference>


const prepare = () => {
	return {
		name: "Transfer",
		next: "yes",
		back: "yes"
	}
}
*/

import Conference_Modal from './Conference_Modal.svelte'

import { onMount } from 'svelte'
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
const modal_store = getModalStore ();


let prepared = "no"

export const enhance = () => {
	
}

const prepare_the_modal = () => {
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: Conference_Modal,
			props: { 
				modal_store
			}
		}
	});
}

onMount (() => {
	prepared = "yes"
	prepare_the_modal ()
})


</script>

<div>
	{ prepared }

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
				>{ name }</header>
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
					<slot name="leaves"></slot>
				
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
</div>