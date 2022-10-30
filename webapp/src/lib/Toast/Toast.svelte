<script lang="ts">
	import {Icon} from "@steeze-ui/svelte-icon";
	import {X} from "@steeze-ui/heroicons";

	export let dismissable = true;
	export let color = '';
	let closed = false;

	let onDismiss = () => {
		closed = true;
	};
</script>

<div class="toast {color}" class:closed class:dismissable>
	<slot />
	{#if dismissable}
		<span class="dismiss" on:click={onDismiss}>
			<Icon src="{X}" slot="icon" />
		</span>
	{/if}
</div>

<style lang="scss">
	@import 'Toast';
</style>
