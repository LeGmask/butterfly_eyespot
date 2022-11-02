<script lang="ts">
	import {api} from "../api";
	import {get} from "svelte/store";
	import {parameters, precursorSquares, solution} from "../stores";
	import Button from "../Button/Button.svelte";
	import {camera} from "../stores.js";
	import Input from "../Input/Input.svelte";

	export let width;
	let disabled = false;

	async function getData() {
		disabled = true;
		const response = await api.post("/run", {
			...get(parameters),
			"A0_pos": $precursorSquares
		});

		$solution = response.data;
		disabled = false;
	}
</script>

<div class="controles" style="width: {width}">
	<h1>Modelling butterfly wing eyespot patterns</h1>
	<div class="flex-container">
		<div class="actions">
			<Button color="accent"
					on:click={() => $parameters.grid = !$parameters.grid}>{$parameters.grid ? 'Hide' : 'show' } grid
			</Button>
			<Button color="accent" on:click={camera.reset}>Reset canvas</Button>
			<Button color="accent" on:click={solution.reset} {disabled}>Reset simulation</Button>
			<!--			<Button color="accent" on:click={parameters.reset}>Reset parameters</Button>-->
			<Button color="accent" on:click={precursorSquares.reset} {disabled}>Reset precursor</Button>
			<Button color="accent" on:click={getData} {disabled}>
				{#if disabled}
					Running...
				{:else}
					Launch a simulation
				{/if}
			</Button>

		</div>

		<h2>Spatial and temporal parameters</h2>
		<div class="parameters">
			<Input bind:value={$parameters.grid_size} class="input" min=0 required={true} type="number" {disabled}>Grid
				size</Input>
			<Input bind:value={$parameters.time_span[0]} class="input" min=0 required={true} type="number" {disabled}>Time
				start</Input>
			<Input bind:value={$parameters.time_span[1]} class="input" min=0 required={true} type="number" {disabled}>Time
				end</Input>
			<Input bind:value={$parameters.time_step} class="input" min=0 required={true} type="number" {disabled}>Time
				step</Input>
		</div>
		<h2>Model parameters</h2>
		<div class="parameters">
			<Input bind:value={$parameters.k1} class="input" min=0 required={true} type="number" {disabled}>k1</Input>
			<Input bind:value={$parameters.k2} class="input" min=0 required={true} type="number" {disabled}>k2</Input>
			<Input bind:value={$parameters.k3} class="input" min=0 required={true} type="number" {disabled}>k3</Input>
			<Input bind:value={$parameters.k4} class="input" min=0 required={true} type="number" {disabled}>k4</Input>
			<Input bind:value={$parameters.k5} class="input" min=0 required={true} type="number" {disabled}>k5</Input>
			<Input bind:value={$parameters.D1} class="input" min=0 required={true} type="number" {disabled}>D1</Input>
			<Input bind:value={$parameters.D2} class="input" min=0 required={true} type="number" {disabled}>D2</Input>
		</div>

		<h2>Initial conditions</h2>
		<div class="parameters">
			<Input bind:value={$parameters.A_0} class="input" min=0 required={true} type="number" {disabled}>A(t=0)</Input>
			<Input bind:value={$parameters.M1_0} class="input" min=0 required={true} type="number" {disabled}>M1(t=0)</Input>
			<Input bind:value={$parameters.M2_0} class="input" min=0 required={true} type="number" {disabled}>M2(t=0)</Input>
			<Input bind:value={$parameters.P0_0} class="input" min=0 required={true} type="number" {disabled}>P0(t=0)</Input>
			<Input bind:value={$parameters.P1_0} class="input" min=0 required={true} type="number" {disabled}>P1(t=0)</Input>
			<Input bind:value={$parameters.P2_0} class="input" min=0 required={true} type="number" {disabled}>P2(t=0)</Input>
			<Input bind:value={$parameters.P0_0_at_foci} class="input" min=0 required={true} type="number" {disabled}>P0(t=0) at foci</Input>
			<Input bind:value={$parameters.A_0_at_foci} class="input" min=0 required={true} type="number" {disabled}>A(t=0) at foci</Input>
		</div>
	</div>
</div>

<style lang="scss">
  @use 'src/scss/colors';

  .controles {
    justify-content: center;
    align-items: center;
    height: calc(100vh - 20px);
    border-radius: 10px;
    width: 100%;
    margin: 10px;
    padding: 20px;
    background-color: colors.$grey-200;
    overflow: scroll;
  }

  h1 {
    font-size: 24px;
    text-align: center;
    font-weight: 500;
    margin: -20px;
    padding: 20px;
    border-radius: 10px 10px 0 0;
    margin-bottom: 20px;
    background-color: colors.$indigo-200;
  }

  .actions {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    width: 100%;
    gap: 5px;
    margin-bottom: 24px;
    flex-wrap: wrap;
    align-items: center;

    //flex-wrap: wrap;
  }

  .flex-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;

  }

  h2 {
    margin: 12px 0;
  }

  .parameters {

    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

</style>