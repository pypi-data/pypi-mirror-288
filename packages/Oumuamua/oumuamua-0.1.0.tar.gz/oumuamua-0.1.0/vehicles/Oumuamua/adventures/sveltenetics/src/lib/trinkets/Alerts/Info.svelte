



<script>


/*
import Info_Alert from '$lib/trinkets/Alerts/Info.svelte'
<Info_Alert 
	text={}
	text_2={}
/>
*/




export let text;
export let text_2 = ""


</script>

{#if typeof text === "string" && text.length >= 1}
<aside 
	class="alert variant-filled-primary" 
	style="
		position: relative;
	
		display: flex; 
		flex-direction: row;
		align-items: center;
		
		padding: 12px; 
		margin-top: 8px
	"
>
	<div 
		class="alert-message" 
		style="
			padding: 0 0 0 10px; 
			margin: 0;
			text-align: center;
		"
	>
		<p>{ text }</p>
		
		{#if text_2.length >= 1}
		<p>{ text_2 }</p>
		{/if}
	</div>
</aside>
{/if}