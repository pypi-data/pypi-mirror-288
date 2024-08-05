




<script>

///
//
//
import Barcode from './Trinkets/Barcode.svelte'
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
import Info_Alert from '$lib/trinkets/Alerts/Info.svelte'
//
import { CodeBlock } from '@skeletonlabs/skeleton';
import { getToastStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { clipboard } from '@skeletonlabs/skeleton';
//
import { onMount, onDestroy } from 'svelte';
import CircleAlert from 'lucide-svelte/icons/circle-alert'
//
//\

import { 
	pick_expiration 
} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/transaction_petition/fields/expiration'

import { 
	create_TP_AO_from_fields
} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/transaction_petition/create/AO_from_fields'

import Progress_Wall from '$lib/trinkets/Progress/Wall/Trinket.svelte'
	

import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land,
	delete_unsigned_transaction
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
//
//\
//\\


/*
	https://github.com/aptos-labs/aptos-ts-sdk/blob/01bf8369f4033996fe5bd20b2172fcad574b1108/src/transactions/types.ts#L100
*/
const prepare_options = ({
	freight
}) => {
	const options = {
		expireTimestamp: pick_expiration ({ 
			after_seconds: freight.fields.transaction_expiration  
		})
	}
	if (freight.fields.use_custom_gas_unit_price === "yes") {
		options.gasUnitPrice = BigInt (freight.fields.gas_unit_price);
	}
	if (freight.fields.use_custom_max_gas_amount === "yes") {
		options.maxGasAmount = BigInt (freight.fields.max_gas_amount);
	}
	
	return options;
}



let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	delete_unsigned_transaction ()
	

	//
	//
	//
	//
	freight.current.land = "Unsigned_Transaction"

	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
	
	try {
		const {
			UTP_AO,
			UTP_hexadecimal_string,
			UTP_stringified,
			
			info_alerts
			
		} = await create_TP_AO_from_fields ({
			net_path: freight.fields.ICANN_net_path,
		
			from_address_hexadecimal_string: freight.fields.from_address_hexadecimal_string,
			to_address_hexadecimal_string: freight.fields.to_address_hexadecimal_string,
			amount: freight.fields.actual_amount_of_Octas,
			
			options: prepare_options ({ freight })
		})
		
		freight.unsigned_transaction.alerts_info = info_alerts;
		
		freight.unsigned_transaction.Aptos_object = UTP_AO;
		freight.unsigned_transaction.hexadecimal_string = UTP_hexadecimal_string
		freight.unsigned_transaction.Aptos_object_fiberized = UTP_stringified
	}
	catch (exception) {
		console.error (exception)
		freight.unsigned_transaction.exception_text = exception.message;
	}
});

onDestroy (() => {
	Truck_Monitor.stop ()
});


let current_format = 0;


let clone_text = "Clone"
let timeout;
const on_clone = async () => {
	clearTimeout (timeout)
	
	clone_text = "Cloned"
	
	await new Promise (resolve => {
		timeout = setTimeout (() => {
			resolve ()
		}, 1000)
	})
	
	clone_text = "Clone"
}


</script>


{#if prepared === "yes"}
<div 
	unsigned_transaction_leaf
	style="
		position: relative;
	"
>
	<section
		style="
			position: relative;
			overflow: scroll;
			padding: .2cm;
		"
	>
		<div
			style="
				text-align: center;
				padding: 0cm 0;
			"
		>
			<header
				style="
					text-align: center;
					font-size: 2em;
					padding: .5cm 0;
				"
			>Transaction Petition</header>
			<p>The consensus require a <b>Transaction Petition</b> with a <b>Transaction Signature</b> to add a transaction to the block chain.</p>
			<p>The <b>Transaction Petition</b> can be signed from the <b>Relatives, Signatures</b> feature by recoding the barcode and then creating a signature from the transaction and a private key.</p>
		</div>
		
		{#if freight.unsigned_transaction.alerts_info.length >= 1 }
		{#each freight.unsigned_transaction.alerts_info as alert_info }
		<Info_Alert 
			text={ alert_info.text }
		/>
		{/each}
		{/if}
		
		{#if freight.unsigned_transaction.exception_text.length >= 1 }
		<aside 
			class="alert variant-filled-error" 
			style="display: flex; flex-direction: row; margin-bottom: 20px; padding: 25px 20px;"
		>
			<div>
				<CircleAlert />
			</div>
			<p style="margin: 0; padding-left: 10px;">{freight.unsigned_transaction.exception_text}</p>
		</aside>
		{/if}
		
		
		
		<div style="height: 12px"></div>
		
		<hr>
		
		<TabGroup justify="justify-center">
			<Tab bind:group={current_format} name="tab1" value={0}>
				<span transaction_as_object_button>Object</span>
			</Tab>
			<Tab bind:group={current_format} name="tab2" value={1}>
				<span transaction_as_hexadecimal_string_button>Hexadecimal</span>
			</Tab>
			<Tab bind:group={current_format} name="tab3" value={2}>
				<span 
					transaction_as_barcode_button
				>Barcode</span>
			</Tab>

			<svelte:fragment slot="panel">
				{#if current_format === 0}
					<div style="text-align: center; padding-bottom: 12px;">
						<p>This is the transaction as an Object.</p>
						<div style="height: 8px"></div>
						<p>For the purpose of showing the object,</p>
						<p>Variables of type <b>Uint8Array</b> were converted into type <b>hexadecimal</b>.</p>
						<p>Variables of type <b>BigInts</b> were converted into type <b>string</b>.</p>
						<div style="height: 8px"></div>
						<p>Those conversions were not applied to the Hexadecimal or Barcode.</p>
					</div>
					
					<div unsigned_transaction_fiberized>
						<Code_Wall 
							text={ freight.unsigned_transaction.Aptos_object_fiberized } 
						/>
					</div>
					
				{:else if current_format === 1}
					<div
						style="
							padding: 0.5cm;
						"
					>
						<p
							style="
								text-align: center;
								padding: 0 0 10px;
							"
						>This is transaction as a hexadecimal string.</p>
						
						
						<div health="UT_Object__UT_hexadecimal_string">
							<Code_Wall 
								can_clone={ "yes" }
								text={ freight.unsigned_transaction.hexadecimal_string } 
							/>
						</div>
					</div>
					
				{:else if current_format === 2}
					<Barcode />
				{/if}
			</svelte:fragment>
		</TabGroup>
	</section>
	
	{#if false }
	<Progress_Wall />
	{/if}
</div>
{/if}