


<script>

import { ConicGradient } from '@skeletonlabs/skeleton';

</script>


<div>
	<ConicGradient 
		stops={[
			{ color: 'transparent', start: 0, end: 25 },
			{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
		]} 
		spin
		width="w-5"
	/>
</div>