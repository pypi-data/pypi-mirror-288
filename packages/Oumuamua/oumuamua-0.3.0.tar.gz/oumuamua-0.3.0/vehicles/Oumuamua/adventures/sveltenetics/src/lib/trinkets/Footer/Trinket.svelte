




<script>

///
///
//
// https://lucide.dev/guide/packages/lucide-svelte#one-generic-icon-component
// https://lucide.dev/icons/
//
//

import { page } from '$app/stores';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { get, writable } from 'svelte/store';
import { onMount, onDestroy } from 'svelte';

import { autoModeWatcher } from '@skeletonlabs/skeleton';
import { setInitialClassState } from '@skeletonlabs/skeleton';

import Bug from 'lucide-svelte/icons/bug'





/*
	<svelte:fragment slot="lead">
		<Bug style="display: inline-block" />
	</svelte:fragment>
*/



</script>



<div>
	<TabGroup 
		justify="justify-center"
		active="variant-filled-primary"
		hover="hover:variant-soft-primary"
		flex="flex-1 lg:flex-none"
		rounded=""
		border=""
	>
		
		<TabAnchor href="/Technicians" selected={ $page.url.pathname.indexOf ('/Technicians') === 0 }>
			<span>Technicians</span>
		</TabAnchor>
		
	</TabGroup>


</div>