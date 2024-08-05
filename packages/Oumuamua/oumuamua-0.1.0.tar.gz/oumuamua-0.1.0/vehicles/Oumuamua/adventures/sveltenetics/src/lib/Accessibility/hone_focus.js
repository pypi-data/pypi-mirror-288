
/*
	import { hone_focus } from '$lib/Accessibility/hone_focus'

	let start_of_panel = ""
	let end_of_panel = ""
	let panel = ""
	let escape_to = ""
	onMount (() => {
		hone_focus ({
			escape_to_element: escape_to,
			after_escape () { console.log ('escaped') },
			
			panel_element: panel,
			first_element: start_of_panel,
			last_element: end_of_panel
		})
	})
*/

/*
const on_key_press_notes = (event) => {
	const control = event.ctrlKey;
	const meta = event.metaKey;
	const alt = event.altKey;
	const shift = event.shiftKey;
	
	const code = event.keyCode;
	const source_element = event.srcElement;
	const target = event.target;
			
	const next_tab = shift === false && code === 9;
	const back_tab = shift === true && code === 9;
	
	const escape = code === 27;
	
	return {
		escape,
		next_tab,
		back_tab
	}
}
*/


const on_key_press = (event) => {
	const shift = event.shiftKey;
	const code = event.keyCode;
	
	const next_tab = shift === false && code === 9;
	const back_tab = shift === true && code === 9;
	const escape = code === 27;
	
	return {
		escape,
		next_tab,
		back_tab
	}
}



export const hone_focus = ({
	first_element,
	last_element,
	
	panel_element,
	escape_to_element = "",
	
	after_escape = () => {},
	
	records = 0
}) => {
	const record = (text) => {
		if (records >= 1) {
			console.log (text)
		}
	}
	
	const escape_from_panel = (event) => {
		record (1, "escape_from_panel");
		
		if (typeof escape_to_element === "object") {
			event.preventDefault ()
			event.stopPropagation ()
			escape_to_element.focus ()
			after_escape ()
		}
	}
	
	panel_element.addEventListener ('keydown', function(event) {
		const { escape } = on_key_press (event)
		if (escape) {
			return escape_from_panel (event)
		}
		
		record (1, "panel: keydown")
	});
	
	//
	//	if back_tab, then go to last element
	//
	//
	first_element.addEventListener ('keydown', function(event) {
		const { back_tab, escape } = on_key_press (event)
		if (escape) {
			return escape_from_panel (event) 
		}		
		
		if (back_tab) {
			event.preventDefault ()
			event.stopPropagation ()
			last_element.focus ()
		}
		
		record (1, { "start of panel: keydown": { back_tab }})
	});
	
	//
	//	if next_tab, then go to first element
	//
	//
	last_element.addEventListener ('keydown', function(event) {
		const { next_tab, escape } = on_key_press (event)
		if (escape) {
			return escape_from_panel (event)
		}
		
		if (next_tab) {
			event.preventDefault ()
			event.stopPropagation ()
			first_element.focus ()
		}

		record (1, { "end of panel: keydown": { event }})
	});
}