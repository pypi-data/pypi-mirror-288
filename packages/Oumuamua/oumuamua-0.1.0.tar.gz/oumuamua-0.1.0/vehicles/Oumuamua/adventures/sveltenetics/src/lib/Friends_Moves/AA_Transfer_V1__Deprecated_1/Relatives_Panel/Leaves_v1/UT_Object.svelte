


<script>

import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
	
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';

///
//
export let unsigned_tx_hexadecimal_string;
export let unsigned_tx_stringified;
export let unsigned_tx_scanned;
//
//\

let unsigned_tx = ""

let current_tab = 0;

</script>


{#if unsigned_tx_stringified.length == 0 }
<div
	style="
		padding: 50px
	"
>
	<p>A barcode picture needs to be scanned to show the unsigned transaction object.</p>
</div>
{:else}
<div>
	<div
		style="
			text-align: center;
			padding: 1cm 0 1cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .2cm 0;
			"
		>Unsigned Transaction</header>
		<p>This unsigned transaction should be the same as the one that was created on the other trinket.</p>
	</div>
	
	<TabGroup>
		<Tab bind:group={current_tab} name="tab1" value={0}>
			<span>Object</span>
		</Tab>
		<Tab bind:group={current_tab} name="tab2" value={1}>
			<span>Hexadecimal</span>
		</Tab>
		
		<svelte:fragment slot="panel">
			{#if current_tab === 0}
				<div>
					<header
						style="
							text-align: center;
							font-size: 1.5em;
							padding: .5cm 0;
						"
					>Unsigned Transaction Object</header>
					<div style="text-align: center">
						<p>For the purpose of showing the object,</p>
						<p>Variables of type <b>Uint8Array</b> were converted into type <b>hexadecimal</b>.</p>
						<p>Variables of type <b>BigInts</b> were converted into type <b>string</b>.</p>
						<div style="height: 8px"></div>
						<p>Those conversions were not applied to the Hexadecimal.</p>
					</div>
					<UT_Stringified 
						unsigned_tx_stringified={ unsigned_tx_stringified }
					/>
				</div>
			{:else if current_tab === 1}
				<div>
					<header
						style="
							text-align: center;
							font-size: 1.5em;
							padding: .5cm 0;
						"
					>Unsigned Transaction Hexadecimal String</header>
					<p
						style="
							text-align: center;
							padding: 10px 0 20px;
						"
					>This is the hexadecimal string of the unsigned transaction.</p>
					<p
						class="bg-surface-50-900-token"
						style="
							white-space: pre-wrap;
							word-wrap: break-word;
							
							box-sizing: border-box;
							height: 100%; 
							font-size: 1em;
							white-space: break-spaces;
							word-wrap: break-word;
							text-align: left;
							padding: 12px;
							border-radius: 4px;
						"
					>{ unsigned_tx_hexadecimal_string }</p>
				</div>
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>
{/if}