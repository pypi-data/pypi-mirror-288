

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

import Net_Trinket from './Trinkets/Net.svelte'
import Relative_Caution_Alert from './Trinkets/Relative_Caution_Alert.svelte'


const tabSet = writable (0);

// @ hints
//		@ students
import { pear } from '@lucide/lab'
import Salad from 'lucide-svelte/icons/salad'

//
// @ Relatives
//
// import Squirrel from 'lucide-svelte/icons/squirrel';
import { cactus, shark, football } from '@lucide/lab'
import Trees from 'lucide-svelte/icons/trees'

//
// @ Friends
//	
//
import TreePalm from 'lucide-svelte/icons/tree-palm';
import Squirrel from 'lucide-svelte/icons/squirrel';
// <Squirrel style="display: inline-block" />
import { palmtreeIslandSun, soccerBall } from '@lucide/lab'
// <TreePalm style="display: inline-block" />
import Rabbit from 'lucide-svelte/icons/rabbit';
import { volleyball } from '@lucide/lab'

//
// 	@ essence
//		@ Habitat, Milieu
//		
import Rocket from 'lucide-svelte/icons/rocket'
import Mountain from 'lucide-svelte/icons/mountain'
import { reelThread, farm } from '@lucide/lab'
import Egg from 'lucide-svelte/icons/egg'
import Satellite from 'lucide-svelte/icons/satellite'
import Activity from 'lucide-svelte/icons/activity'
import SunMoon from 'lucide-svelte/icons/sun-moon'

// @ Roomies
import Bug from 'lucide-svelte/icons/bug'



// import Door from 'lucide-svelte/icons/door';
import DoorOpen from 'lucide-svelte/icons/door-open'
import CircleAlert from 'lucide-svelte/icons/circle-alert'
import Message_Circle_Warning from 'lucide-svelte/icons/message-circle-warning'
import Construction from 'lucide-svelte/icons/construction'
import TrafficCone from 'lucide-svelte/icons/traffic-cone';
import Soda from 'lucide-svelte/icons/cup-soda'
import Piano from 'lucide-svelte/icons/piano';
import Wheat from 'lucide-svelte/icons/wheat'

import Music4 from 'lucide-svelte/icons/music-4'


// import UFO from 'lucide-svelte/lab/ufo'
// import Tire from 'lucide-svelte/lab/tire'

import PawPrint from 'lucide-svelte/icons/paw-print'
import CircuitBoard from 'lucide-svelte/icons/circuit-board'
import ScanQRCode from 'lucide-svelte/icons/scan-qr-code'


import { planet, chameleon, spiderWeb } from '@lucide/lab'


let currentTile = -1;

import { Icon } from 'lucide-svelte';

/*
<svelte:fragment slot="lead">
	<SunMoon style="display: inline-block" />
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
		<TabAnchor href="/" selected={$page.url.pathname === '/' }>
			<span>Scholars</span>
		</TabAnchor>
		<TabAnchor href="/Friends" selected={ $page.url.pathname.indexOf ('/Friends') === 0 }>
			<span>Friends</span>
		</TabAnchor>
		<TabAnchor href="/Relatives" selected={ $page.url.pathname.indexOf ('/Relatives') === 0 }>
			<span>Relatives</span>
		</TabAnchor>
		<TabAnchor href="/Roomies" selected={ $page.url.pathname.indexOf ('/Roomies') === 0 }>
			<span>Roomies</span>
		</TabAnchor>
	</TabGroup>
	
	
	{#if $page.url.pathname.indexOf ('/Friends') === 0 }
	<div>
		<TabGroup 
			justify="justify-center"
			active="variant-filled-primary"
			hover="hover:variant-soft-primary"
			flex="flex-1 lg:flex-none"
			rounded=""
			border=""
			class="bg-surface-100-800-token w-full"
		>			
			<TabAnchor href="/Friends" selected={$page.url.pathname === '/Friends'}>
				<span>Hints</span>
			</TabAnchor>
			<TabAnchor 
				href="/Friends/Consensus" 
				selected={$page.url.pathname === '/Friends/Consensus'}
			>
				<span>Consensus</span>
			</TabAnchor>
			<TabAnchor 
				href="/Friends/Moves" 
				selected={$page.url.pathname.indexOf ('/Friends/Moves') === 0 }
			>
				<span>Moves</span>
			</TabAnchor>
		</TabGroup>
	</div>
	{:else if (
		$page.url.pathname === '/'
	)}
	<div>
		<TabGroup 
			justify="justify-center"
			active="variant-filled-primary"
			hover="hover:variant-soft-primary"
			flex="flex-1 lg:flex-none"
			rounded=""
			border=""
			class="bg-surface-100-800-token w-full"
		>			
			<TabAnchor 
				href="/Guests"
				selected={
					$page.url.pathname.indexOf ('/Guests') === 0 ||
					$page.url.pathname === '/'
				}
			>
				<span>Hints</span>
			</TabAnchor>
		</TabGroup>
	</div>
	{:else if $page.url.pathname.indexOf ('/Relatives') === 0}
	<div>
		<TabGroup 
			justify="justify-center"
			active="variant-filled-primary"
			hover="hover:variant-soft-primary"
			flex="flex-1 lg:flex-none"
			rounded=""
			border=""
			class="bg-surface-100-800-token w-full"
		>			
			<TabAnchor href="/Relatives" selected={$page.url.pathname === '/Relatives'}>
				<span>Hints</span>
			</TabAnchor>
			<TabAnchor 
				href="/Relatives/Addresses/Address_Origin_Map" 
				selected={
					$page.url.pathname.indexOf ('/Relatives/Addresses') === 0
				}
			>
				<span>Addresses</span>
			</TabAnchor>
			<TabAnchor href="/Relatives/Signatures" selected={$page.url.pathname === '/Relatives/Signatures'}>
				<ScanQRCode style="display: inline-block" />
				<span>Signatures</span>
			</TabAnchor>
		</TabGroup>
	</div>
	{:else if $page.url.pathname.indexOf ('/Roomies') === 0}
	<div>
		<TabGroup 
			justify="justify-center"
			active="variant-filled-primary"
			hover="hover:variant-soft-primary"
			flex="flex-1 lg:flex-none"
			rounded=""
			border=""
			class="bg-surface-100-800-token w-full"
		>			
			<TabAnchor href="/Roomies" selected={$page.url.pathname === '/Roomies'}>
				<span>Hints</span>
			</TabAnchor>
			<TabAnchor 
				href="/Roomies/Plays" 
				selected={$page.url.pathname.indexOf ('/Roomies/Plays') === 0}
			>
				<span>Plays</span>
			</TabAnchor>
		</TabGroup>
	</div>
	{:else}
	<div></div>
	{/if}
	
	
	
	
	{#if $page.url.pathname.indexOf ('/Relatives/Addresses') === 0 }
	<div>
		<TabGroup 
			justify="justify-center"
			active="variant-filled-primary"
			hover="hover:variant-soft-primary"
			flex="flex-1 lg:flex-none"
			rounded=""
			border=""
			class="bg-surface-100-800-token w-full"
		>			
			<TabAnchor 
				href="/Relatives/Addresses/Address_Origin_Map" 
				selected={ 
					$page.url.pathname === '/Relatives/Addresses/Address_Origin_Map'
				}
			>
				<span>Address Origin Map</span>
			</TabAnchor>
		</TabGroup>
	</div>
	{/if}
	
	<Net_Trinket />
	
	{#if $page.url.pathname.indexOf ('/Relatives') === 0 }
	<Relative_Caution_Alert />
	{/if}
	
</div>