



<script>

import { SlideToggle } from '@skeletonlabs/skeleton';

let permitted = false;

const refresh_storage = () => {
	localStorage.clear ();
	sessionStorage.clear ();
	window.location.reload ();
}

</script>


<div>
	<div
		class="card p-4"
		style="
			display: flex;
			align-items: center;
			justify-content: center;
			flex-direction: column;
		"
	>
		<header
			style="
				font-size: 1.4em;
				line-height: 200%;
			"
		>Browser Storage</header>
		<div style="width: 10px"></div>
		<p>The <b>Refresh</b> button clears the browser storage.</p>
		<div style="height: 6px"></div>
		<p>To permit refresh, the slide needs to in the <b>permit</b> position.</p>
		<div style="height: 6px"></div>
		
		<div
			style="
				display: flex;
				align-items: center;
				justify-content: center;
				
				padding: 20px;
			"
		>
			<p
				style="
					padding: 8px;
				"
			>deny</p>
			<SlideToggle 
				name="slide" 
				bind:checked={ permitted } 
			/>
			<p
				style="
					padding: 8px;
				"
			>permit</p>
		</div>
		
		<div
			style="
				display: flex;
				align-items: center;
				justify-content: center;
				gap: 8px;
			"
		>
			<button 
				on:click={ refresh_storage }
				disabled={ permitted != true }
				type="button" 
				class="btn variant-filled-error"
			>Refresh</button>
		</div>
	</div>

</div>