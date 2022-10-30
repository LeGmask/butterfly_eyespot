import {writable} from "svelte/store";
import type {Solution} from "../types/Solution.type";
import type {Square} from "../types/Square.type";
import type {Parameters} from "../types/Parameters.type";

function createSolution() {
	const {subscribe, set, update} = writable<Solution | null>(null);

	return {
		subscribe,
		set,
		update,
		reset: () => set(null),
	}
}

function createPrecursorSquares() {
	const {subscribe, set, update} = writable<Square[]>([]);

	return {
		subscribe,
		set,
		update,
		reset: () => set(null),
	}
}

function createParameters() {
	let default_parameters: Parameters = {
		grid_size: 21,
		time_span: [0, 15],
		time_step: 0.1,

		k1: 1.0,
		k2: 0.05,
		k3: 4.0,
		k4: 0.01,
		k5: 4.0,
		D1: 0.002,
		D2: 0.002,

		A_0: 0,
		M1_0: 0,
		M2_0: 0,
		P0_0: 0.2,
		P1_0: 0,
		P2_0: 0,
		P0_0_with_precursor: 0,
		A0_0_with_precursor: 20
	}
	const {subscribe, set, update} = writable<Parameters>(default_parameters);

	return {
		subscribe,
		set,
		update,
		reset: () => set(default_parameters),
	}
}

export const solution = createSolution();
export const precursorSquares = createPrecursorSquares();
export const parameters = createParameters();