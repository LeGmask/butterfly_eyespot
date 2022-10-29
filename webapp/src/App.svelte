<script lang="ts">
	import {Canvas, Layer, t} from "svelte-canvas";

	export let grid_size = 51;

	let zoom = 1;
	let camera = {x: 0, y: 0};
	let isDragging = false;
	let dragStart = {x: 0, y: 0};


	$: render = ({context, width, height}) => {
		context.strokeStyle = "lightgrey";

		context.scale(zoom, zoom);
		context.translate(camera.x, camera.y);

		let grid_width = Math.floor(width / grid_size);
		let grid_height = Math.floor(height / grid_size);

		// draw grid shape
		context.beginPath();

		for (let x = 0; x <= grid_size; x++) {
			context.moveTo(x * grid_height, 0);
			context.lineTo(x * grid_height, grid_size * grid_height);

		}

		for (let y = 0; y <= grid_size; y++) {
			context.moveTo(0, y * grid_width);
			context.lineTo(grid_size * grid_width, y * grid_width);
		}

		context.stroke();

		requestAnimationFrame(() => {
			context.resetTransform();
			context.fillStyle = "white";
			context.font = "20px Arial";
			context.fillText(`Zoom: ${zoom}`, 10, 30);
			context.fillText(`Camera: ${camera.x}, ${camera.y}`, 10, 60);
		});
	};

	function handleMouseDown(event) {
		isDragging = true;
		dragStart = {x: event.clientX, y: event.clientY};
	}

	function handleMouseUp(event) {
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
		zoom += event.deltaY / 1000;
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
</Canvas>