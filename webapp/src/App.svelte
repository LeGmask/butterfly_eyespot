<script lang="ts">
	import Square from "./lib/Grid/Square.svelte";
	import {parameters, precursorSquares} from "./lib/stores.js";
	import GridCanvas from "./lib/Grid/GridCanvas.svelte";
	import Grid from "./lib/Grid/Grid.svelte";
	import GridSolution from "./lib/Grid/GridSolution.svelte";
	import Controles from "./lib/Controles/Controles.svelte";

	let innerWidth = window.innerWidth;
	let innerHeight = window.innerHeight;
	let dim: number; // we need to use a watcher to update this

	$: dim = Math.min(innerWidth, innerHeight) - 20;


</script>

<svelte:window bind:innerWidth bind:innerHeight/> <!-- bind:innerWidth bind:innerHeight in case window is resized... -->

<div class="flex-container">
	<GridCanvas debug={false} {dim}>
		<GridSolution/>

		{#each $precursorSquares as [x, y]}
			<Square x={x} y={y}/>
		{/each}

		{#if $parameters.grid}
			<Grid grid_size={$parameters.grid_size}/>
		{/if}
	</GridCanvas>

	<Controles width={
		innerWidth - dim - 20
	}/>
</div>

<style lang="scss">
  .flex-container {
    display: flex;
    flex-direction: row;
    //align-items: center;
    //flex-wrap: wrap;
  }
</style>

