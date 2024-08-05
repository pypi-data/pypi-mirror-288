

/*
	import { make_barcode } from '$lib/Barcode/make'
	make_barcode ({
		barcode_element,
		hexadecimal_string: ""
	})
*/



import { BrowserQRCodeSvgWriter } from '@zxing/browser';

export const make_barcode = ({
	barcode_element, 
	hexadecimal_string,
	size = 500
}) => {
	const code_writer = new BrowserQRCodeSvgWriter ()
	
	// console.log ({ code_writer })
	
	const SVG_Element = code_writer.writeToDom (
		barcode_element, 
		hexadecimal_string, 
		size, 
		size
	)
}