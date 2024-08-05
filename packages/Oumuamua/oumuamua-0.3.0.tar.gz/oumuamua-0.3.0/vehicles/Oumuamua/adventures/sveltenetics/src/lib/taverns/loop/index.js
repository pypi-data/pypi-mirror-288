

/*
	import { loop } from '$lib/taverns/loop'
	 
	const loop_1 = loop ({
		wait: 2000,
		action: () => {
		 
		}
	})
	
	loop_1.play ()
	loop_1.stop ()
	loop_1.play ()
*/

/*
	import { loop } from '$lib/taverns/loop'
	
	const loop_1 = loop ({
		wait: 2000,
		wait_for_response: "yes",
		action: async () => {
		 
		}
	})
	
	loop_1.play ()
	loop_1.stop ()
	loop_1.play ()
*/


export const loop = ({
	wait,
	action,
	wait_for_response = "no"
}) => {
	let playing = "no"
	
	let timeout = ""
	const the_loop = async () => {
		if (playing === "yes") {
			if (wait_for_response === "yes") {
				try {
					await action ();
				}
				catch (exception) {
					console.error (exception)
				}
			}
			else {
				setTimeout (() => {
					action ();
				})
			}
		}
		
		await new Promise (resolve => {
			timeout = setTimeout (() => {
				resolve ()
			}, wait)
		})
		
		if (playing === "yes") {
			clearTimeout (timeout)
			the_loop ();
		}
	}
	
	return {
		play: () => {
			if (playing === "no") {
				playing = "yes"
				the_loop ()
			}
		},
		/*pause: () => {
			clearTimeout (timeout)
			playing = "no"
		},*/
		stop: () => {
			clearTimeout (timeout)
			playing = "no"
		}
	}
}