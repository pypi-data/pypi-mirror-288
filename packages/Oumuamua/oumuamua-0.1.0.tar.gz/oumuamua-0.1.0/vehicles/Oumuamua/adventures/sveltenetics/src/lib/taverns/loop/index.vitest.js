
// vitest "lib/taverns/loop/index.vitest.js"


import { loop } from './index.js'
import { describe, it, expect } from 'vitest';

import assert from 'assert'


// await wait (1000)
const wait = async (duration) => {
	await new Promise (resolve => {
		setTimeout (() => {
			resolve ()
		}, duration)
	})
}

describe ("loop", () => {
	it ("loops", async () => {
		let loops_run = 0
		
		const loop_1 = loop ({
			wait: 250,
			action: () => {
				loops_run += 1
			}
		})
		
		loop_1.play ()
		
		// 0
		await wait (125)
		loop_1.stop ()
		assert.equal (loops_run, 1)
		
		
		// 0, 250
		loop_1.play ()
		await wait (375)
		loop_1.stop ()
		assert.equal (loops_run, 3)
		
		// 0, 250, 500
		loop_1.play ()
		await wait (625)
		loop_1.stop ()
		assert.equal (loops_run, 6)
	})
})

describe ("loop async", () => {
	it ("loops", async () => {
		let loops_run = 0
		
		const loop_1 = loop ({
			wait: 40,
			wait_for_response: "yes",
			action: async () => {
				loops_run += 1
				await wait (40)
			}
		})
		
		loop_1.play ()
		
		// 0, 80
		await wait (120)
		loop_1.stop ()
		assert.equal (loops_run, 2)
		
		
		// 0, 80, 160
		loop_1.play ()
		await wait (200)
		loop_1.stop ()
		assert.equal (loops_run, 5)
		
		// 0, 80, 160, 240
		loop_1.play ()
		await wait (280)
		loop_1.stop ()
		assert.equal (loops_run, 9)
	})
})