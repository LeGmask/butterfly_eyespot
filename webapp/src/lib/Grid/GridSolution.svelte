<script lang="ts">
	import Square from "./Square.svelte";
	import {solution} from "../stores.js";

	function getMaxPigment(P0, P1, P2) {
		let output = []
		for (let i = 0; i < P0.length; i++) {
			let currentRow = []
			for (let j = 0; j < P0[i].length; j++) {
				let data = [P0[i][j], P1[i][j], P2[i][j]]
				// get the index of the max value
				let maxIndex = data.indexOf(Math.max(...data))
				currentRow.push(maxIndex)
			}
			output.push(currentRow)
		}
		return output
	}

	function indexToColor(index) {
		switch (index) {
			case 0:
				return "#70420E"
			case 1:
				return "#040404"

			case 2:
				return "#BFA440"

			default:
				return "#ffffff"
		}
	}
</script>

{#if $solution}
	{#each getMaxPigment($solution.P0, $solution.P1, $solution.P2) as row, i}
		{#each row as col, j}
			<Square x={j} y={i} color={indexToColor(col)}/>
		{/each}
	{/each}
{/if}