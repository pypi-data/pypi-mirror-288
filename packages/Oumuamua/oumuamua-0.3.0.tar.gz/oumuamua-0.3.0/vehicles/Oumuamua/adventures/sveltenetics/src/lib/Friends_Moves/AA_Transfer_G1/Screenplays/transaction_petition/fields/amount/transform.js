

/*
	import { convert_integer_to_Uint8Array_amount } from '../amount/transform'
	const u_int_8_array = convert_integer_to_Uint8Array_amount (10000000)
*/

/*
	import { convert_Uint8Array_to_integer_amount } from '../amount/transform'
	const integer_amount = convert_Uint8Array_to_integer_amount ()
*/

export const convert_integer_to_Uint8Array_amount = ({ integer_amount }) => {
	const u_int_8_array = new Uint8Array (8); // 8 bytes
	u_int_8_array.set (
		new Uint8Array (
			new BigUint64Array ([
				BigInt (integer_amount)
			]).buffer
		)
	);
		
	return u_int_8_array;
}

//
//	const the_integer = new Uint8Array ([255, 0, 0, 0, 0, 0, 0, 0]);
//
//
export const convert_Uint8Array_to_integer_amount = ({ u_int_8_array }) => {
	const view = new DataView (u_int_8_array.buffer);
	return view.getBigUint64 (0, true); // true for little-endian
}