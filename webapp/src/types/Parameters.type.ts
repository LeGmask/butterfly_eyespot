export type Parameters = {
	// simulation parameters
	grid_size: number;
	time_span: [number, number];
	time_step: number;

	// numerical parameters
	k1: number;
	k2: number;
	k3: number;
	k4: number;
	k5: number;
	D1: number;
	D2: number;

	// initial conditions
	A_0: number;
	M1_0: number;
	M2_0: number;
	P0_0: number;
	P1_0: number;
	P2_0: number;
	P0_0_with_precursor: number;
	A0_0_with_precursor: number;
}