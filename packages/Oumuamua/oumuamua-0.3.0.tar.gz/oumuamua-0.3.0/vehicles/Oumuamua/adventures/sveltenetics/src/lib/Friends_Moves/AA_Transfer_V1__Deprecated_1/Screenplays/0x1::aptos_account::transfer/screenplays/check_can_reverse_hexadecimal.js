



export const check_can_reverse_hexadecimal = ({
	transaction_petition
}) => {
	const transaction_petition_as_bytes = transaction_petition.bcsToBytes ()
	const transaction_petition_hexadecimal_string = string_from_Uint8Array (transaction_petition_as_bytes)
	
}