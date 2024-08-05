


<script>

/*	
	import Amount_Field from '$lib/trinkets/Amount_Field/Trinket.svelte'
	
	const on_amount_change = ({ 
		effects,
		actual_amount_of_Octas
	}) => {
		if (effects.problems === "") {
			
		}
	}
	
	<Amount_Field 
		on_change={ on_amount_change }
	/>
*/

///
//
import Problem_Alert from '$lib/trinkets/Alerts/Problem.svelte'
//
import { onMount, onDestroy } from 'svelte';
import Big from 'big.js'
import { ask_convert_APT_to_Octas } from '$lib/origin/math/APT_to_Octas.RPC.js'
import { Octas_string_is_permitted } from './Screenplays/Octas_string_is_permitted.js'
//
import { has_field } from 'procedures/object/has_field'
//
//\

export let on_change = () => {}
export let verify = () => {}
export let after_mount = () => {}

import { build_truck } from '$lib/trucks'
const trucks = {}

$: amount = "1"
$: currency = "APT"

$: actual_amount_of_Octas = ""

let effects = {
	sci_note_estimate_of_Octas: "",	
	problem: ""
}

$: {
	let _amount = amount;
	effect_change ()
}
$: {
	let _currency = currency;
	effect_change ()
}
$: {
	let _actual_amount_of_Octas = actual_amount_of_Octas;
	calculate_exponent ()
}

const Octas_from_APT = async () => {
	let proceeds = ""
	
	try {
		const { enhanced } = await ask_convert_APT_to_Octas ({
			APT: amount.toString ()
		})
		if (enhanced.victory === "yes") {
			actual_amount_of_Octas = enhanced.Octas;
			on_change ({
				effects,
				actual_amount_of_Octas,
				
				amount,
				currency
			})
			return;
		}
		else {
			if (has_field (enhanced, "note")) {
				effects.problem = enhanced.note;
			}
			else {
				effects.problem = verify ({
					merch,
					effects
				})
			}
		}
	}
	catch (exception) {
		effects.problem = exception.message;
	}
	
	actual_amount_of_Octas = ""
	
	on_change ({
		effects,
		actual_amount_of_Octas,
		
		amount,
		currency
	})
}



const effect_change = async () => {
	// console.info ('effect_change', currency, amount)
	
	effects.problem = ""
	actual_amount_of_Octas = ""
	
	try {
		if (currency === "APT") {
			await Octas_from_APT ();				
			return;
		}
		
		if (currency === "Octas") {
			const Octas_as_string = amount.toString ();
			if (Octas_string_is_permitted (Octas_as_string) !== "yes") {
				effects.problem = `Octas needs to be a natural number. (1, 2, 3, 4, 5, ...)`
				return;
			}
			
			actual_amount_of_Octas = Octas_as_string;
			
			on_change ({
				effects,
				actual_amount_of_Octas,
				
				amount,
				currency
			})
			return;
		}
		
		effects.problem = `Currency "${currency}" was not accounted for.`
		return;
	}
	catch (exception) {
		effects.problem = exception.message;
	}
	
	on_change ({
		effects,
		actual_amount_of_Octas,
		
		amount,
		currency
	})
}

let prepared = "no"
onMount (async () => {
	await after_mount ();
	
	effect_change ()
	
	prepared = "yes"
})

onDestroy (() => {})

const calculate_exponent = () => {1
	// console.log ({ calculate_exponent })

	try {
		let exponent = parseFloat (actual_amount_of_Octas).toExponential () 
		if (exponent === "NaN") {
			return ""
		}
		
		// console.log ({ exponent })
		
		return exponent;
	}
	catch (exception) {
		console.error (exception)
	}

	return ""
}

</script>

{#if prepared === "yes"}
<div>
	<label class="label">
		<aside class="alert variant-filled-warning">
			<div class="alert-message"
				style="
					text-align: center;
				"
			>
				<p><b>Caution</b>, Please make sure "<b>Actual Octas Amount</b>" is the intended amount.
				<p>It's calculated from the number provided and is the amount used.</p>
			</div>
		</aside>
		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="padding: 2px"
		>
			<select 
				currency_chooser
			
				bind:value={ currency }
				
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
				amount_field
				
				bind:value={ amount }
				
				style="padding: 10px; border: 0"
				class="input" 
				
				type="text" 
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
		<div class="card p-4" style="width: 290px">
			<span>Octas, Sci Note Estimate</span>
		</div>
		<div style="width: 10px"></div>
		<div class="card p-4" style="width: 100%">
			<span>{
				calculate_exponent (actual_amount_of_Octas)
			}</span>
		</div>
	</div>

	<div
		style="
			display: flex;
			width: 100%;
			margin-top: 10px;
		"
	>
		<div class="card p-4" style="width: 290px">
			<span><b>Actual Octas Amount</b></span>
		</div>
		<div style="width: 10px"></div>
		<div class="card p-4" style="width: 100%">
			<span actual_amount_of_octas>{ actual_amount_of_Octas }</span>
		</div>
	</div>
	
	<Problem_Alert 
		text={ effects.problem }
	/>
</div>
{/if}