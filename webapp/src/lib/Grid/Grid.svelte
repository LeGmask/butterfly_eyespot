<script lang="ts">
	import {Layer} from "svelte-canvas";
	import {parameters} from "../stores";

	$: render = ({context, width, height}) => {
		context.strokeStyle = "lightgray";
		let grid_width = Math.floor(width / $parameters.grid_size);
		let grid_height = Math.floor(height / $parameters.grid_size);

		// draw grid shape
		context.beginPath();

		for (let x = 0; x <= $parameters.grid_size; x++) {
			context.moveTo(x * grid_height, 0);
			context.lineTo(x * grid_height, $parameters.grid_size * grid_height);

		}

		for (let y = 0; y <= $parameters.grid_size; y++) {
			context.moveTo(0, y * grid_width);
			context.lineTo($parameters.grid_size * grid_width, y * grid_width);
		}

		context.stroke();
	};
</script>

<Layer {render}/>