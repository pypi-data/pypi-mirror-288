



const verify_UTP_hexadecimal_string = ({
	TP_hexadecimal_string,
	TP_unpacked_hexadecimal_string
}) => {
	if (TP_hexadecimal_string !== TP_unpacked_hexadecimal_string) {
		throw new Error (JSON.stringify ({
			"note": "The original transaction petition hexadecimal string is not equal to the unpacked version.",
			TP_hexadecimal_string,
			TP_unpacked_hexadecimal_string
		}, null, 4))
	}
}