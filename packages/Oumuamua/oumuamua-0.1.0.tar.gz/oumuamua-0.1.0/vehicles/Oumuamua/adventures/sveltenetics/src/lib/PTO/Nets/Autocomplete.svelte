

<script>
	
//	import Nets_Autocomplete from '$lib/PTO/Nets/Autocomplete.svelte'	
	
import { Autocomplete } from '@skeletonlabs/skeleton';
import { popup } from '@skeletonlabs/skeleton';

let popupSettings = {
	event: 'focus-click',
	target: 'popupAutocomplete',
	placement: 'bottom',
};


const flavorOptions = [
	{ 
		label: 'mainnet', 
		value: 'devnet'
	},
	{ 
		label: 'testnet', 
		value: 'devnet'
	},
	{ 
		label: 'devnet', 
		value: 'devnet'
	}
];			

let inputPopupDemo = '';

const onPopupDemoSelect = (packet) => {
	console.log (packet)
}


let value = '';
const items = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'];




</script>					

<div>
	<input
		class="input autocomplete"
		type="search"
		name="autocomplete-search"
		bind:value={ inputPopupDemo }
		placeholder="Search..."
		use:popup={ popupSettings }
	/>
	<div data-popup="popupAutocomplete">
		<Autocomplete
			bind:input={ inputPopupDemo }
			options={ flavorOptions }
			on:selection={ onPopupDemoSelect }
		/>
	</div>

</div>