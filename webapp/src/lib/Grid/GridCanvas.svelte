<script lang="ts">
	import {Canvas, Layer} from "svelte-canvas";
	import {camera, parameters, precursorSquares} from "../stores";
	import {get} from "svelte/store";

	export let debug = false;
	export let dim

	let canvas: Canvas;
	let isDragging = false;
	let dragStart = {x: 0, y: 0};

	let mouseDownPos = {x: 0, y: 0};

	$: render = ({context}) => {
		context.scale($camera.zoom, $camera.zoom);
		context.translate($camera.x, $camera.y);

		requestAnimationFrame(() => {
			context.resetTransform();

			if (debug) {
				context.fillStyle = "white";
				context.font = "20px Arial";
				context.fillText(`Zoom: ${camera.zoom}`, 10, 30);
				context.fillText(`Camera: ${$camera.x}, ${$camera.y}`, 10, 60);
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
			$camera.x += (event.clientX - dragStart.x) / $camera.zoom;
			$camera.y += (event.clientY - dragStart.y) / $camera.zoom;
			dragStart = {x: event.clientX, y: event.clientY};
		}

	}

	function handleWheel(event) {
		$camera.zoom -= event.deltaY / 1000;
		$camera.zoom = Math.max(0.1, $camera.zoom);
	}

	function handleClick(event) {
		const ctx: CanvasRenderingContext2D = canvas.getContext()
		let grid_square_width = Math.floor(ctx.canvas.width / $parameters.grid_size);

		let grid_square_height = Math.floor(ctx.canvas.height / $parameters.grid_size);
		// if the mouse has moved more than 10px, don't add a square
		if (isDragging &&
			Math.abs(mouseDownPos.x - event.clientX) > 10 ||
			Math.abs(mouseDownPos.y - event.clientY) > 10) {
			return;

		}
		// compute position of the square in function of camera and zoom

		let targetedPoint = [
			Math.floor(((event.clientX - 10) / $camera.zoom - $camera.x) / grid_square_width),
			Math.floor(((event.clientY - 10) / $camera.zoom - $camera.y) / grid_square_height)
		];
		// if the square isn't in the grid, don't add it
		if (targetedPoint[0] < 0 || targetedPoint[0] >= $parameters.grid_size ||
			targetedPoint[1] < 0 || targetedPoint[1] >= $parameters.grid_size) {
			return;

		}
		// if the square is already in the grid, remove it
		if ($precursorSquares.some(([x, y]) => x === targetedPoint[0] && y === targetedPoint[1])) {
			$precursorSquares = [...$precursorSquares.filter(([x, y]) => x !== targetedPoint[0] || y !== targetedPoint[1])];
		} else {
			$precursorSquares = [...$precursorSquares, targetedPoint];
		}

	}

</script>


<Canvas bind:this={canvas} width={dim} height={dim} on:mousemove={handleMouseMove} on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp} on:wheel={handleWheel} on:click={handleClick} class="canvas">
	<Layer {render}/>

	<slot/>
</Canvas>

<style lang="scss">
  @use "src/scss/colors";

  :global(canvas) {
    margin: 10px;
    background-color: colors.$grey-1000;
    //border-radius: 10px;
    //padding: 20px;
  }
</style>
