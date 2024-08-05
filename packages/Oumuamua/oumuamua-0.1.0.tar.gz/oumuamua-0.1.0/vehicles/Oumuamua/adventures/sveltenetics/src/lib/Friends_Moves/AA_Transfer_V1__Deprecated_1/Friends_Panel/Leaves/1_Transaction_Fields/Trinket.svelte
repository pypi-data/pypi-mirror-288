



<script>


////
///
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
import { getToastStore } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
import Net_Choices from '$lib/PTO/Nets/Choices.svelte'
//
import Amount_Field from '$lib/trinkets/Amount_Field/Trinket.svelte'
import Address_Qualities_Trinket from '$lib/trinkets/Address_Qualities/Trinket.svelte'
//
import Input_Error_Message from '$lib/Friends_Moves/AA_Transfer_G1/Trinkets/Input_Error_Message.svelte'
//
import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
//
//\
//\\


let prepared = "no"
let Truck_Monitor;
let freight;
onMount (() => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	//
	//
	//
	//
	freight.current.land = "Transaction_Fields"

	Truck_Monitor = monitor_truck ((freight) => {
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	prepared = "yes"
});

onDestroy (() => {
	Truck_Monitor.stop ()
});

let net_name = ""
const on_change = ({ net }) => {
	net_name = net.name;
	const net_path = net.path;
	
	freight.fields.ICANN_net_path = net.path;
	freight.fields.net_name = net.name;
}


const on_amount_change = ({ 
	effects,
	actual_amount_of_Octas
}) => {
	console.log ("on_amount_change", actual_amount_of_Octas)
	
	if (effects.problem === "") {
		freight.fields.actual_amount_of_Octas = actual_amount_of_Octas;
	}
}

const styles = {
	header: parse_styles ({
		
	})
}




let origin_address_trinket = ""
const on_prepare_origin_address = () => {
	origin_address_trinket.change_address_hexadecimal_string (
		freight.fields.from_address_hexadecimal_string
	)
}
const on_change_origin_address = ({
	effective,
	address_hexadecimal_string,
	exception
}) => {
	freight.fields.from_address_permitted = effective;
	freight.fields.from_address_exception = exception;
	freight.fields.from_address_hexadecimal_string = address_hexadecimal_string;
}


let to_address_trinket = ""
const on_prepare_to_address = () => {
	to_address_trinket.change_address_hexadecimal_string (
		freight.fields.to_address_hexadecimal_string
	)
}
const on_change_to_address = ({
	effective,
	address_hexadecimal_string,
	exception
}) => {
	freight.fields.to_address = effective;
	freight.fields.to_address = exception;
	freight.fields.to_address_hexadecimal_string = address_hexadecimal_string;
}


/*
<tr>
	<td>
		<header style="text-align: center; font-size: 1.2em; padding: padding: 0 0 8px">From Address</header>
		<textarea 
			from_aptos_address
			class="textarea"
			style="min-height: 50px; padding: 10px"
			bind:value={ freight.fields.from_address_hexadecimal_string }
			type="text" 
			placeholder=""
			
			rows="1"
		/>
	</td>
</tr>
<tr>
	<td>
		<header style="text-align: center; font-size: 1.2em; padding: 0 0 8px">To Address</header>
		<textarea 
			to_aptos_address
			class="textarea"
			style="min-height: 50px; padding: 10px"
			bind:value={ freight.fields.to_address_hexadecimal_string }
			type="text" 
			placeholder=""
			
			rows="1"
		/>
	</td>
</tr>
*/

</script>


<style>

td {
	display: flex;
	flex-direction: column;
}

p {
	white-space: normal;
}

</style>

{#if prepared === "yes"}
<div>
	<div 
		style="padding: 0.5cm 0"
	>
		<p
			style="text-align: center; font-size: 1em"
		>This is for transfering Octas from one address to another address.</p>
		<p
			style="text-align: center; font-size: 1em"
		>The contract is:</p>
		<p style="text-align: center; font-size: 1em">
			<b>0x1::aptos_account::transfer</b>
		</p>
	</div>
	
	<section>		
		<div class="table-container">
			<table class="table table-hover">
				<tbody>
					<tr>
						<td address-chooser-td>
							<header style="text-align: center; font-size: 1.2em; padding: padding: 0 0 8px">Address (ICANN)</header>
							<Net_Choices
								net_name={ freight.fields.net_name }
								on_change={ on_change }
							/>
							
							<div style="height: 6px"></div>
							
							{#if net_name === "custom" }
							<textarea 
								icann_net_address
								
								bind:value={ freight.fields.ICANN_net_path }
								
								class="textarea"
								style="min-height: 50px; padding: 10px"
								type="text" 
								placeholder=""
							/>
							{:else}
							<div class="card p-4">
								<span icann_net_address>{ freight.fields.ICANN_net_path }</span>
							</div>
							{/if}
						</td>
					</tr>
					<tr>
						<td>
							<Address_Qualities_Trinket 
								name="From Address"
								bind:this={ origin_address_trinket }
								on_change={ on_change_origin_address }
								on_prepare={ on_prepare_origin_address }
							/>
						</td>
					</tr>
					<tr>
						<td>
							<Address_Qualities_Trinket 
								name="To Address"
								bind:this={ to_address_trinket }
								on_change={ on_change_to_address }
								on_prepare={ on_prepare_to_address }
							/>
						</td>
					</tr>
					
					<tr>
						<td>							
							<header style="text-align: center; font-size: 1.2em; padding: 0">Amount</header>
							<p
								style="text-align: center; padding-bottom: 10px"
							>1 APT = 1e8 Octas</p>
							
							<Amount_Field 
								on_change={ on_amount_change }
							/>
							
							<div style="display: none">
								<label class="label" >
									<div 
										class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
										style="padding: 2px"
									>
										<select 
											currency_chooser
										
											bind:value={ freight.fields.currency }
											class="input-group-shim"
											style="
												width: 100px;
												border-top-left-radius: 20px;
												border-bottom-left-radius: 20px;	
												text-align: center;
											"
										>
											<option>APT</option>
											<option>Octas</option>
										</select>
										<input 
											amount
											
											bind:value={ freight.fields.amount  }
											
											style="padding: 10px; border: 0"
											class="input" 
											
											type="number" 
											placeholder="Amount of Octas" 
										/>
									</div>
								</label>
								
								<div
									style="
										display: flex;
										width: 100%;
										margin-top: 10px;
									"
								>
									<div class="card p-4" style="width: 250px">
										<span>Actual Amount of Octas</span>
									</div>
									<div style="width: 10px"></div>
									<div class="card p-4" style="width: 100%">
										<span>{ freight.fields.actual_amount_of_Octas }</span>
									</div>
								</div>
								
								<Input_Error_Message 
									text={ freight.fields.problems.amount }
								/>
							</div>
						</td>
					</tr>
					<tr>
						<td>
							<header style="text-align: center; font-size: 1.2em; padding: 10px 0">Transaction Expiration, in seconds</header>
							<label class="label"
								style="display: flex; align-items: center;"
							>
								<input 
									class="input"
									style="text-indent: 10px; padding: 10px" 
									
									transaction_expiration
									placeholder="" 
									
									type="number" 
									bind:value={ freight.fields.transaction_expiration }
								/>
							</label>
						</td>
					</tr>
					<tr>
						<td>
							<header style="text-align: center; font-size: 1.2em; padding: 10px 0">Gas Unit Price, in Octas</header>
							<label class="label"
								style="display: flex; align-items: center;"
							>
								<input 
									class="input"
									style="text-indent: 10px; padding: 10px" 
									
									transaction_expiration
									placeholder="" 
									
									type="number" 
									bind:value={ freight.fields.gas_unit_price }
								/>
							</label>
						</td>
					</tr>
					<tr>
						<td>
							<header style="text-align: center; font-size: 1.2em; padding: 10px 0">Max Gas Amount, in Octas</header>
							<label class="label"
								style="display: flex; align-items: center;"
							>
								<input 
									class="input"
									style="text-indent: 10px; padding: 10px" 
									
									transaction_expiration
									placeholder="" 
									
									type="number" 
									bind:value={ freight.fields.max_gas_amount }
								/>
							</label>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</section>
</div>
{/if}