

import { parse_styles } from '$lib/trinkets/styles/parse.js';

export const make_trends = () => {
	const trends = {
		textarea: parse_styles ({
			border: "4px solid black",
			"border-radius": "4px",
			"margin": "10px 0",
			"padding": "5px",
			
			// "box-shadow": '0 0 0 2px white, 0 0 0 0px black',
			
			"width": "100%",
			"background": "none"
		}),
		action: parse_styles ({
			// border: "4px solid black",
			"border-radius": "4px",
			"margin": "10px 0",
			"padding": "5px",
			
			// "box-shadow": '0 0 0 2px white, 0 0 0 0px black',
			
			"width": "100%"
		}),
		decal: parse_styles ({
			display: 'inline-block',
			'border-right': "4px solid black",
			'border-bottom': "4px solid black",
			
			"border-top-right-radius": "0%",
			"border-bottom-right-radius": "4px",
			
			"padding": "5px 10px",
			
			
		}),
		hexadecimal_seed: parse_styles ({
			display: 'block',
			"word-wrap": "anywhere"
		})
	}
	
	return trends;
}