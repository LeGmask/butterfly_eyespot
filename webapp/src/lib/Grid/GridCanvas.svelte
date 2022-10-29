<script lang="ts">
	import {Canvas, Layer} from "svelte-canvas";
	import Square from "./Square.svelte";
	import Grid from "./Grid.svelte";

	export let grid_size = 21;
	export let debug = false;

	let zoom = 1;
	let camera = {x: 0, y: 0};
	let isDragging = false;
	let dragStart = {x: 0, y: 0};


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


	let innerWidth = window.innerWidth
	let innerHeight = window.innerHeight

	let dim

	$: dim = Math.min(innerWidth, innerHeight)
</script>

<svelte:window bind:innerWidth bind:innerHeight/>

<Canvas width={dim} height={dim} on:mousemove={handleMouseMove} on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp} on:wheel={handleWheel}>
	<Layer {render}/>
	<Grid {grid_size}/>
	<Square x={10} y={10} {grid_size}/>
</Canvas>