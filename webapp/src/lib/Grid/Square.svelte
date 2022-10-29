<script lang="ts">
	import {Layer} from "svelte-canvas";

	export let x: number;
	export let y: number;

	export let grid_size: number;
	export let color: string = "white";


	$: render = ({context, width, height}) => {
		let grid_square_width = Math.floor(width / grid_size);
		let grid_square_height = Math.floor(height / grid_size);

		context.fillStyle = color;

		context.fillRect(x * grid_square_width, y * grid_square_height, grid_square_width, grid_square_height);
	}
</script>

<Layer {render}/>
