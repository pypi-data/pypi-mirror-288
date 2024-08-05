
//
//	import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//

//
//	nibble: 4 bits, for example: 0, 1, .., F
//	byte:   8 bits, for example: 00, 01, ... , EF, FF
//

/*
	byte_to_hexadecimal ("0A")
*/
function byte_to_hexadecimal (byte) {
    return ('0' + byte.toString(16).toUpperCase()).slice(-2);
}


//
//	Uint8Array.from ([ 0, 255, 256, -1 ]) -> [ 0, 255, 0, 255 ]
//
export const Uint8Array_from_string = (hexadecimal_string) => {
	//
	//	"00" = 0
	//	"FF" = 255
	//
	//	Therefore if "FF0", then isn't possible to convert to Uint8Array
	//
	if (hexadecimal_string.length % 2 !== 0) {		
		throw new Error (`The hexadecimal string "${ hexadecimal_string }" does not divide by 2.`)
	}
	
	const byte_integers = []
	
	let E = -2;
	while ((E += 2) < hexadecimal_string.length) {
		const nibble_1 = Number ("0x" + hexadecimal_string [ E + 1 ]);
		const nibble_2 = Number ("0x" + hexadecimal_string [ E ]) * 16;
		
		const byte_integer = (nibble_1 + nibble_2)
		if (isNaN (byte_integer)) {
			throw new Error (`The nibbles at indexes ${ E } & ${ E + 1 } did not convert into a byte integer.`)
		}
		
		byte_integers.push (byte_integer)
	}

	
	return Uint8Array.from (byte_integers)
}