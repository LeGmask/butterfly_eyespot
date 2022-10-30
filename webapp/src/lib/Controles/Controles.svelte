<script lang="ts">
	import {api} from "../api";
	import {get} from "svelte/store";
	import {parameters, precursorSquares, solution} from "../stores";
	import Button from "../Button/Button.svelte";
	import {camera} from "../stores.js";
	import Input from "../Input/Input.svelte";

	export let width

	async function getData() {
		const response = await api.post("/run", {
			...get(parameters),
			"A0_pos": $precursorSquares
		});

		$solution = response.data;
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
			<Button color="accent" on:click={solution.reset}>Reset simulation</Button>
			<Button color="accent" on:click={parameters.reset}>Reset parameters</Button>
			<Button color="accent" on:click={precursorSquares.reset}>Reset precursor</Button>
		</div>

		<div class="parameters">
			<Input bind:value={$parameters.grid_size} class="input" min=0
				   required={true} type="number">Grid size</Input>
			<Input bind:value={$parameters.time_span[0]} class="input" min=0
				   required={true} type="number">Time start</Input>
			<Input bind:value={$parameters.time_span[1]} class="input" min=0
				   required={true} type="number">Time end</Input>
			<Input bind:value={$parameters.time_step} class="input" min=0
				   required={true} type="number">Time step</Input>
			<Input bind:value={$parameters.k1} class="input" min=0
				   required={true} type="number">k1</Input>
			<Input bind:value={$parameters.k2} class="input" min=0
				   required={true} type="number">k2</Input>
			<Input bind:value={$parameters.k3} class="input" min=0
				   required={true} type="number">k3</Input>
			<Input bind:value={$parameters.k4} class="input" min=0
				   required={true} type="number">k4</Input>
			<Input bind:value={$parameters.k5} class="input" min=0
				   required={true} type="number">k5</Input>
			<Input bind:value={$parameters.D1} class="input" min=0
				   required={true} type="number">D1</Input>
			<Input bind:value={$parameters.D2} class="input" min=0
				   required={true} type="number">D2</Input>
		</div>

		<div class="run">
			<Button color="accent" on:click={getData}>Launch a simulation</Button>
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
    //flex-wrap: wrap;
  }

  .flex-container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;

  }

  .run {
    //margin: 140% 0 0 0;
  }

</style>