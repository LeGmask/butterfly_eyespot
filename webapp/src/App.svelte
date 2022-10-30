<script lang="ts">
	import {api} from "./lib/api";
	import Square from "./lib/Grid/Square.svelte";
	import {solution} from "./lib/stores";
	import {parameters, precursorSquares} from "./lib/stores.js";
	import GridCanvas from "./lib/Grid/GridCanvas.svelte";
	import Grid from "./lib/Grid/Grid.svelte";
	import GridSolution from "./lib/Grid/GridSolution.svelte";
	import {get} from "svelte/store";

	let innerWidth = window.innerWidth;
	let innerHeight = window.innerHeight;
	let dim: number; // we need to use a watcher to update this

	$: dim = Math.min(innerWidth, innerHeight);


	async function getData() {
		const response = await api.post("/run", {
			...get(parameters),
			"A0_pos": $precursorSquares
		});

		$solution = response.data;
	}
</script>

<svelte:window bind:innerWidth bind:innerHeight/> <!-- bind:innerWidth bind:innerHeight in case window is resized... -->

<GridCanvas debug={true} {dim}>
	{#if $solution}
		<GridSolution/>
	{/if}

	{#each $precursorSquares as [x, y]}
		<Square x={x} y={y}/>
	{/each}

	<Grid grid_size={$parameters.grid_size}/>
</GridCanvas>

<button on:click={getData}>get data</button>
