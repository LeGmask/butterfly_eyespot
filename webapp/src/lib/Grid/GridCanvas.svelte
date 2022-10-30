<script lang="ts">
	import {Canvas, Layer} from "svelte-canvas";
	import Square from "./Square.svelte";
	import Grid from "./Grid.svelte";
	import axios from "axios";
	import {api} from "../api";
	import type {Solution} from "../../types/Solution.type";

	let solution: Solution;

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


	export let grid_size = 10;
	export let debug = false;

	let canvas: Canvas;
	export let squares: Array<[number, number]> = []

	let zoom = 1;
	let camera = {x: 0, y: 0};
	let isDragging = false;
	let dragStart = {x: 0, y: 0};
	let mouseDownPos = {x: 0, y: 0};


	$: render = ({context}) => {
		context.scale(zoom, zoom);
		context.translate(camera.x, camera.y);

		requestAnimationFrame(() => {
			context.resetTransform();

			if (debug) {
				context.fillStyle = "white";
				context.font = "20px Arial";
				context.fillText(`Zoom: ${zoom}`, 10, 30);
				context.fillText(`Camera: ${camera.x}, ${camera.y}`, 10, 60);
			}
		});
	};

	function handleMouseDown(event) {
		isDragging = true;
		dragStart = {x: event.clientX, y: event.clientY};
		mouseDownPos = {x: event.clientX, y: event.clientY};
	}

	function handleMouseUp() {
		isDragging = false;
	}

	function handleMouseMove(event: MouseEvent) {
		if (isDragging) {
			camera.x += (event.clientX - dragStart.x) / zoom;
			camera.y += (event.clientY - dragStart.y) / zoom;
			dragStart = {x: event.clientX, y: event.clientY};
		}
	}

	function handleWheel(event) {
		zoom -= event.deltaY / 1000;
		zoom = Math.max(0.1, zoom);
	}

	function handleClick(event) {
		const ctx: CanvasRenderingContext2D = canvas.getContext()
		let grid_square_width = Math.floor(ctx.canvas.width / grid_size);
		let grid_square_height = Math.floor(ctx.canvas.height / grid_size);

		// if the mouse has moved more than 10px, don't add a square
		if (isDragging &&
			Math.abs(mouseDownPos.x - event.clientX) > 10 ||
			Math.abs(mouseDownPos.y - event.clientY) > 10) {
			return;
		}

		// compute position of the square in function of camera and zoom
		let targetedPoint = [
			Math.floor((event.clientX / zoom - camera.x) / grid_square_width),
			Math.floor((event.clientY / zoom - camera.y) / grid_square_height)
		];

		// if the square isn't in the grid, don't add it
		if (targetedPoint[0] < 0 || targetedPoint[0] >= grid_size ||
			targetedPoint[1] < 0 || targetedPoint[1] >= grid_size) {
			return;
		}

		// if the square is already in the grid, remove it
		if (squares.some(([x, y]) => x === targetedPoint[0] && y === targetedPoint[1])) {
			squares = [...squares.filter(([x, y]) => x !== targetedPoint[0] || y !== targetedPoint[1])];
		} else {
			squares = [...squares, targetedPoint];
		}
	}

	function getIndexMax(arr) {
		if (arr.length === 0) {
			return -1;
		}

		let max = arr[0];
		let maxIndex = 0;

		for (let i = 1; i < arr.length; i++) {
			if (arr[i] > max) {
				maxIndex = i;
				max = arr[i];
			}
		}

		return maxIndex;
	}

	async function getData() {
		const response = await api.post("/run", {
			"grid_size": grid_size,
			"A0_pos": squares
		});
		solution = response.data;
	}

	let innerWidth = window.innerWidth
	let innerHeight = window.innerHeight

	let dim

	$: dim = Math.min(innerWidth, innerHeight)
</script>

<svelte:window bind:innerWidth bind:innerHeight/>

<Canvas bind:this={canvas} width={dim} height={dim} on:mousemove={handleMouseMove} on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp} on:wheel={handleWheel} on:click={handleClick}>
	<Layer {render}/>

	{#if solution}
		{#each getMaxPigment(solution.P0, solution.P1, solution.P2) as row, i}
			{#each row as col, j}
				<Square x={j} y={i} {grid_size} color={indexToColor(col)}/>
			{/each}
		{/each}
	{/if}
	{#each squares as [x, y]}
		<Square x={x} y={y} {grid_size}/>
	{/each}
	<Grid bind:grid_size/>

</Canvas>

<button on:click={getData}>get data</button>