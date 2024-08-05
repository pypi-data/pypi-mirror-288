
<script>


// import Input_Error_Message from '$lib/Friends_Moves/AA_Transfer_G1/Trinkets/Input_Error_Message.svelte'

import { ConicGradient } from '@skeletonlabs/skeleton';

export let text;

const conicStops = [
	{ color: 'transparent', start: 0, end: 25 },
	{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
];

</script>

{#if typeof text === "string" && text.length >= 1}
<aside 
	class="alert variant-soft-error" 
	style="display: flex; padding: 8px; margin-top: 8px"
>
	<ConicGradient stops={conicStops} spin 
		width="w-6"
	/>
	<div class="alert-message">
		<p>{ text }</p>
	</div>
</aside>
{/if}