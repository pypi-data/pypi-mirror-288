



<script>


/*
import Problem_Alert from '$lib/trinkets/Alerts/Problem.svelte'
<Problem_Alert 
	text={}
/>
*/

// https://wavesurfer.xyz/

/*
<ConicGradient stops={conicStops} spin 
	width="w-6"
/>
*/


import { onMount } from 'svelte'
import { ConicGradient } from '@skeletonlabs/skeleton';
import Eternal_1_Progress from '$lib/trinkets/Progress/Eternal_1/Trinket.svelte'

export let text;

const conicStops = [
	{ color: 'transparent', start: 0, end: 25 },
	{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
];

onMount (() => {})

let wait_color = document.documentElement.classList.contains ("dark") ? "#000000" : "#FF0000";

</script>

{#if typeof text === "string" && text.length >= 1}
<aside 
	class="alert variant-filled-error" 
	style="
		display: flex; 
		flex-direction: row;
		align-items: center;
		
		padding: 12px; 
		margin-top: 8px
	"
>	
	<Eternal_1_Progress 
		width={ "50px" } 
		height={ "35px" }
		color={ wait_color }
	/>
	
	<div class="alert-message" style="padding: 0 0 0 10px; margin: 0;">
		<p>{ text }</p>
	</div>
</aside>
{/if}