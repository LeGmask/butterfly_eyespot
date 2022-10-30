import {writable} from "svelte/store";
import type {Solution} from "../types/Solution.type";
import type {Square} from "../types/Square.type";

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

export const solution = createSolution();
export const precursorSquares = createPrecursorSquares();