

<script lang="ts">
	import { SvelteComponent } from 'svelte';

	import { ListBox, ListBoxItem, getModalStore } from '@skeletonlabs/skeleton';

	// Props
	/** Exposes parent props to this component. */
	export let parent;

	// Local
	let flavor = 'faucet';
	const modalStore = getModalStore();

	// Handle Form Submission
	function onFormSubmit() {
		if ($modalStore[0].response) $modalStore[0].response(flavor);
		modalStore.close ();
	}

	// Base Classes
	const cBase = 'card p-4 w-modal shadow-xl space-y-4';
	const cHeader = 'text-2xl font-bold';
</script>

<!-- @component This example creates a simple form modal. -->

{#if $modalStore[0]}
	<div class="modal-example-form {cBase}">
		<header class={cHeader} style="text-align: center">Moves</header>
		<ListBox class="border border-surface-500 p-4 rounded-container-token">
			<ListBoxItem bind:group={flavor} name="faucet" value="faucet">Faucet</ListBoxItem>
			<ListBoxItem bind:group={flavor} name="APT Give" value="APT_Send">APT Give</ListBoxItem>
		</ListBox>
		<!-- prettier-ignore -->
		<footer class="modal-footer {parent.regionFooter}">
        <button class="btn {parent.buttonNeutral}" on:click={parent.onClose}>{parent.buttonTextCancel}</button>
        <button class="btn {parent.buttonPositive}" on:click={onFormSubmit}>Choose</button>
    </footer>
	</div>
{/if}