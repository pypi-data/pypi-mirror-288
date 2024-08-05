


export const calculate_Uint8Array_amount = ({ integer_amount }) => {
	const byteArray1 = new Uint8Array (8); // 8 bytes
	byteArray1.set (
		new Uint8Array (
			new BigUint64Array ([
				BigInt (integer_amount)
			]).buffer
		)
	);
	
	console.log(byteArray1); // Logs: Uint8Array(8) [ 255, 0, 0, 0, 0, 0, 0, 0 ]

}

//
//	const byteArray1 = new Uint8Array ([255, 0, 0, 0, 0, 0, 0, 0]);
//
//
export const calculate_Uint8Array_amount = ({ u_int_8_array }) => {
	const view = new DataView(array.buffer);
	return view.getBigUint64 (0, true); // true for little-endian
}