from typing import List, Tuple

import numpy as np
import scipy
from scipy.integrate import solve_ivp

# @TODO: Add docstring
# @TODO: Add type hints
# @TODO: clean up code (ie refactor)

class Model:
	def __init__(self, shape: int = 101, time_span: Tuple[float, float] = (0, 15),
				 time_step: float = 0.1, k1=1.0, k2=0.05, k3=4.0,
				 k4=0.01, k5=4.0, D1=0.002, D2=0.002):
		self.shape = shape
		self.D2 = D2
		self.D1 = D1
		self.k5 = k5
		self.k4 = k4
		self.k3 = k3
		self.k2 = k2
		self.k1 = k1
		self.solution = None
		self.time_vector = np.arange(time_span[0], time_span[1], time_step)
		self.A0_pos: List[(int, int)] | None = None

	@staticmethod
	def laplacian_2d(u, h):
		stencil = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]]) / h ** 2

		return scipy.ndimage.convolve(u, stencil, mode='mirror')

	def function_test(self, t, u, h, A0: np.ndarray, ):
		M1, M2, P0, P1, P2 = self.restore_dimension(u)

		A = A0 * np.exp(-self.k1 * t)

		dM1_dt = self.k1 * A - self.k2 * M1 - self.k3 * M1 * P0 + self.D1 * Model.laplacian_2d(M1, h)
		dM2_dt = self.k3 * M1 * P0 - self.k4 * M2 - self.k5 * M2 * P0 + self.D2 * Model.laplacian_2d(M2, h)
		dP0_dt = -self.k3 * M1 * P0 - self.k5 * M2 * P0
		dP1_dt = self.k3 * M1 * P0
		dP2_dt = self.k5 * M2 * P0

		return np.concatenate((dM1_dt, dM2_dt, dP0_dt, dP1_dt, dP2_dt)).flatten()

	def restore_dimension(self, u: np.ndarray) -> List[np.ndarray]:
		return np.split(u.reshape(self.shape * 5, self.shape), 5)

	def solve(self):
		h = 1 / self.shape

		y0, A0 = self.get_initial_conditions()

		self.solution = solve_ivp(self.function_test, (self.time_vector[0], self.time_vector[-1]), y0, args=(h, A0),
								  t_eval=self.time_vector)

	def get_initial_conditions(self, M1: float = 0, M2: int = 0, P0: int = 0.2, P1: int = 0, P2: int = 0, A=0,
							   P0_active=0.2, A_active=20) -> Tuple[np.ndarray, np.ndarray]:
		M1 = np.full((self.shape, self.shape), M1)
		M2 = np.full((self.shape, self.shape), M2)
		P0 = np.full((self.shape, self.shape), P0)
		P1 = np.full((self.shape, self.shape), P1)
		P2 = np.full((self.shape, self.shape), P2)

		A0 = np.full((self.shape, self.shape), A)

		if self.A0_pos is not None:
			for pos in self.A0_pos:
				A0[pos[0], pos[1]] = A_active
				P0[pos[0], pos[1]] = P0_active

		return np.concatenate((M1, M2, P0, P1, P2)).flatten(), A0

	def append_A0_pos(self, pos: Tuple[int, int] | List[Tuple[int, int]]):
		if self.A0_pos is None:
			self.A0_pos = []

		if isinstance(pos, list):
			self.A0_pos.extend(pos)
		else:
			self.A0_pos.append(pos)

	def remove_A0_pos(self, pos: Tuple[int, int] | List[Tuple[int, int]]):
		if self.A0_pos is None:
			return

		if isinstance(pos, list):
			for p in pos:
				self.A0_pos.remove(p)
		else:
			self.A0_pos.remove(pos)
