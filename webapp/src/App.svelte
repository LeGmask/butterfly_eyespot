<script lang="ts">
	import {api} from "./lib/api";
	import Square from "./lib/Grid/Square.svelte";
	import {solution} from "./lib/stores";
	import {precursorSquares} from "./lib/stores.js";
	import GridCanvas from "./lib/Grid/GridCanvas.svelte";
	import Grid from "./lib/Grid/Grid.svelte";
	import GridSolution from "./lib/Grid/GridSolution.svelte";

	let grid_size = 21;


	async function getData() {
		const response = await api.post("/run", {
			"grid_size": grid_size,
			"A0_pos": $precursorSquares
		});
		$solution = response.data;
	}
</script>

<GridCanvas grid_size={grid_size} debug={true}>
	{#if $solution}
		<GridSolution {grid_size}/>
	{/if}

	{#each $precursorSquares as [x, y]}
		<Square x={x} y={y} {grid_size}/>
	{/each}

	<Grid bind:grid_size/>
</GridCanvas>

<button on:click={getData}>get data</button>
