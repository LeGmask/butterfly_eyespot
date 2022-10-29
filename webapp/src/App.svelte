<script lang="ts">
	import {Canvas, Layer, t} from "svelte-canvas";

	let zoom = 1;
	let camera = {x: 0, y: 0};
	let isDragging = false;
	let dragStart = {x: 0, y: 0};


	$: render = ({context, width, height}) => {
		context.strokeStyle = "lightgrey";

		context.scale(zoom, zoom);
		context.translate(camera.x, camera.y);

		let grid_size = 101;
		let grid_width = Math.ceil(width / grid_size);
		let grid_height = Math.ceil(height / grid_size);

		// draw grid shape
		context.beginPath();

		for (let x = 0; x < grid_size; x++) {
			context.moveTo(x * grid_height, 0);
			context.lineTo(x * grid_height, height);

		}

		for (let y = 0; y < grid_size; y++) {
			context.moveTo(0, y * grid_width);
			context.lineTo(width, y * grid_width);
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
			camera.x += event.clientX / zoom - dragStart.x;
			camera.y += event.clientY / zoom - dragStart.y;
			dragStart = {x: event.clientX, y: event.clientY};
		}
	}


	let innerWidth = window.innerWidth
	let innerHeight = window.innerHeight
</script>

<svelte:window bind:innerWidth bind:innerHeight/>
<Canvas width={800} height={800} on:mousemove={handleMouseMove} on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp}>
	<Layer {render}/>
</Canvas>