
// bun run vitest "src/lib/trinkets/elyptic_keyy/screenplays/hexadecimalize.vitest.js"


import { hexadecimalize } from './hexadecimalize'
//
import { describe, it, expect } from 'vitest';
import assert from 'assert'


describe ('hexadecimalize', () => {
	it ('is consistent', async () => {
		const {
			private_key_choosen,
			score,
			note,
			
			hexadecimal_private_key,
			hexadecimal_public_key,
			hexadecimal_address
		} = await hexadecimalize ({
			original: "SGOWYTKDHGUFIDOSYGLEYTIFJDSLGYOWOTLDHSDFGORUDKOSYWHGJJHOFIEEYFKT",
			nibble_count: 64
		})
		
		console.log ({
			hexadecimal_private_key,
			hexadecimal_public_key,
			hexadecimal_address
		})
		
		assert.equal (
			hexadecimal_private_key,
			"8B7043E9CB5A69784BF1436AD98FB47073F9C89AB7259E7840CBDDC7A6114AE3"
		)
		assert.equal (
			hexadecimal_public_key,
			"DE1E9343E13395075EA2F2E1C2564B1A1109D5120B09F01FC221EC246A9A5CB6"
		)
		assert.equal (
			hexadecimal_address,
			"4B7DB0C742D38FE030457A9E5C11F49FDD4EBC312F3D3E07094D81BF4EB706D2"
		)
	});
});
