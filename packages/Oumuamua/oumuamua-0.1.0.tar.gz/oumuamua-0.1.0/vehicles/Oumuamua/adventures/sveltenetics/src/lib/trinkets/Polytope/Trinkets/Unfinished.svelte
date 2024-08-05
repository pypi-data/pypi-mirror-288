



<script>

import { onMount, onDestroy } from 'svelte';
import { fade } from 'svelte/transition';

export let close = () => {}
export let showing = "no"

</script>


{#if showing === "yes"}
<div
	transition:fade
	unfinished-extravaganza
	class="card"
	style="
		display: block;
		position: absolute;
		top: 10px;
		left: 10px;
		
		width: calc(100% - 20px);
		height: calc(100% - 90px);
		
		opacity: 1;
		border-radius: 8px;
		
		z-index: 9999;
	"
>
	<div
		style="
			position: absolute;
			top: 0;
			left: 0;
			
			width: 100%;
			height: 100%;
			
			display: flex;
		"
	>
		<main
			style="
			position: absolute;
				top: 0;
				left: 0;
				
				width: 100%;
				height: calc(100% - 60px);
				
				display: flex;
				align-items: center;
				justify-content: center;
			"
		>
			<slot></slot>
		</main>
		<footer
			style="
				position: absolute;
				bottom: 0;
				left: 0;
			
				height: 60px;
				width: 100%;
				padding: 8px;
				
				display: flex;
				justify-content: right;
			"
		>
			<button 
				class="btn variant-filled" 
				on:click={ close }
			>
				Close
			</button>
		</footer>
	</div>
</div>
{/if}
