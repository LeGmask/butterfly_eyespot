from typing import List, Tuple

import numpy as np
import scipy
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from scipy.integrate import solve_ivp


class Model:
	def __init__(self, grid_size: int = 101, time_span: Tuple[float, float] = (0, 15), time_step: float = 0.1, k1=1.0,
				 k2=0.05, k3=4.0, k4=0.01, k5=4.0, D1=0.002, D2=0.002, M1_0: float = 0, M2_0: float = 0,
				 P0_0: float = 0.2,
				 P1_0: float = 0, P2_0: float = 0, A_0=0, P0_0_at_foci: float = 0,
				 A_0_at_foci: float = 20) -> None:
		"""
		The __init__ function is called when an instance of the class is created.
		It initializes the attributes of the class.
		
		:param grid_size:int=101: Define the size of the grid
		:param time_span: Set the time interval of the simulation
		:param time_step:float=0.1: Specify the time step of the solution
		:param k1=1.0: Set the value of k1
		:param k2=0.05: Set the value of k2
		:param k3=4.0: Set the value of k3
		:param k4=0.01: Set the value of k4
		:param k5=4.0: Set the value of k5
		:param D1=0.002: Set the diffusion rate of M1
		:param D2=0.002: Set the diffusion rate of M2
		:param M1_0:float=0: Set the initial value of M1
		:param M2_0:float=0: Set the initial value of M2
		:param P0_0:float=0.2: Set the initial value of p0
		:param P1_0:float=0: Set the initial value of p1
		:param P2_0:float=0: Set the initial value of p2
		:param A_0=0: Set the initial value of A
		:param P0_0_at_foci:float=0.2: Set the initial value of p0 at the foci
		:param A_0_at_foci:float=20: Set the initial value of A at the foci
		:return: None
		"""
		self.shape = grid_size

		self.A_0 = A_0
		self.M1_0 = M1_0
		self.M2_0 = M2_0
		self.P0_0 = P0_0
		self.P1_0 = P1_0
		self.P2_0 = P2_0

		self.k1 = k1
		self.k2 = k2
		self.k3 = k3
		self.k4 = k4
		self.k5 = k5

		self.D1 = D1
		self.D2 = D2

		self.A_0_at_foci = A_0_at_foci
		self.P0_0_at_foci = P0_0_at_foci

		self.solution = None
		self.time_vector = np.arange(time_span[0], time_span[1] + time_step, time_step)
		self.foci_pos: List[(int, int)] | None = None

	@staticmethod
	def laplacian_2d(u: np.ndarray, h: float) -> np.ndarray:
		"""
		The laplacian_2d function computes an approximation of the 2D laplacian in a 2D array.
		
		:param u:np.ndarray: Pass the u array to the function
		:param h:float: Define the step of the grid
		:return: The approximation of the 2D laplacian of u, obtained by the convolution of u with the 2D laplacian stencil
		"""
		stencil = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]]) / h ** 2

		return scipy.ndimage.convolve(u, stencil, mode='mirror')

	def eyespot_system(self, t, u, A0: np.ndarray) -> np.ndarray:
		M1, M2, P0, _, _ = self.restore_dimension(u)

		A = A0 * np.exp(-self.k1 * t)

		dM1_dt = self.k1 * A - self.k2 * M1 - self.k3 * M1 * P0 + self.D1 * Model.laplacian_2d(M1, 1 / self.shape)
		dM2_dt = self.k3 * M1 * P0 - self.k4 * M2 - self.k5 * M2 * P0 + self.D2 * Model.laplacian_2d(M2, 1 / self.shape)
		dP0_dt = -self.k3 * M1 * P0 - self.k5 * M2 * P0
		dP1_dt = self.k3 * M1 * P0
		dP2_dt = self.k5 * M2 * P0

		return np.concatenate((dM1_dt, dM2_dt, dP0_dt, dP1_dt, dP2_dt)).flatten()

	def restore_dimension(self, u: np.ndarray) -> List[np.ndarray]:
		"""
		The restore_dimension function takes a vector of length 5 * self.shape and reshapes it into the original
		self.shape array.
		
		:param u:np.ndarray: Pass the input to the function
		:return: A list of the 5 arrays that are the result of reshaping u
		"""
		return np.split(u.reshape(self.shape * 5, self.shape), 5)

	def solve(self):
		"""
		The solve function solves the system of differential equations that describe
		the dynamics of the model. It takes as input a list of time points to evaluate
		at, and returns a solution object containing information about how the variables
		change over time. The solve function also accepts an optional argument A0, which is 
		a vector containing initial conditions for A.
		
		:return: A solution object, which contains the following:
		"""
		y0, A0 = self.get_initial_conditions()

		self.solution = solve_ivp(self.eyespot_system, (self.time_vector[0], self.time_vector[-1]), y0, args=(A0,),
								  t_eval=self.time_vector)

	def get_initial_conditions(self) -> Tuple[np.ndarray, np.ndarray]:
		"""
		The get_initial_conditions function returns a tuple of two arrays. T
		he first array is the initial conditions for all variables in the system, and the second array is the initial  condition for A  at each point in space.
		Also the initial conditions for the foci are set if there are foci.
		
		:return: y0 and A0
		"""
		M1 = np.full((self.shape, self.shape), self.M1_0)
		M2 = np.full((self.shape, self.shape), self.M2_0)
		P0 = np.full((self.shape, self.shape), self.P0_0)
		P1 = np.full((self.shape, self.shape), self.P1_0)
		P2 = np.full((self.shape, self.shape), self.P2_0)

		A0 = np.full((self.shape, self.shape), self.A_0)

		if self.foci_pos is not None:
			for pos in self.foci_pos:
				A0[pos[0], pos[1]] = self.A_0_at_foci
				P0[pos[0], pos[1]] = self.P0_0_at_foci

		return np.concatenate((M1, M2, P0, P1, P2)).flatten(), A0

	def append_foci(self, pos: Tuple[int, int] | List[Tuple[int, int]]) -> None:
		"""
		The append_foci function adds a position to the list of foci positions.
		If the foci_pos attribute is None, then it creates an empty list and appends
		the position to that. If it's not None, then it just appends the position.
		
		:param self: Reference the object itself, i
		:param pos: Specify the position of a foci
		:return: None
		"""
		if self.foci_pos is None:
			self.foci_pos = []

		if isinstance(pos, list):
			self.foci_pos.extend(pos)
		else:
			self.foci_pos.append(pos)

	def remove_foci(self, pos: Tuple[int, int] | List[Tuple[int, int]]) -> None:
		"""
		The remove_foci function removes the given position from the list of foci.
		If a list is passed in, all positions in the list are removed.
		
		:param pos: Specify the position of the foci to delete or a list of positions
		:return: None
		"""
		if self.foci_pos is None:
			return

		if isinstance(pos, list):
			for p in pos:
				self.foci_pos.remove(p)
		else:
			self.foci_pos.remove(pos)

	def sync_foci(self, pos: Tuple[int, int] | List[Tuple[int, int]]) -> None:
		"""
		The sync_foci function overrides foci from the model, by setting the given position to the list of foci.
		If a list is passed in, all positions in the list are added.

		:param pos: Specify the position of the foci to sync or a list of positions
		:return: None
		"""
		if self.foci_pos is None:
			self.foci_pos = []

		self.foci_pos = pos if isinstance(pos, list) else [pos]

	@staticmethod
	def get_pigment_matrix(P0: np.ndarray, P1: np.ndarray, P2: np.ndarray) -> np.ndarray:
		"""
		The get_pigment_matrix function takes in three 2D arrays of the same size and returns a 2D array of the same size.
		The function iterates through each element in P0, P2, and P2 to find which value is largest.  If all values are 0,
		the function returns 0 for that element. Otherwise it returns 1 if the max value was found in P0, 2 if the max
		value was found in P1 or 3 if it was found in P2.

		:param P0:np.ndarray: Matrix of value in space of pigment 0.
		:param P1:np.ndarray: Matrix of value in space of pigment 1.
		:param P2:np.ndarray: Matrix of value in space of pigment 2.
		:return: The maximum value in each pixel of the three arrays
		"""
		color = np.empty(P0.shape)

		for (x, y), value in np.ndenumerate(P0):
			color[x, y] = np.argmax(np.array([P0[x, y], P1[x, y], P2[x, y]])) + 1 if sum(
				[P0[x, y], P1[x, y], P2[x, y]]) != 0 else 0

		return color

	def show(self) -> FuncAnimation:
		"""
		The show function is a helper function that creates an animation of the model.
		It uses matplotlib to create a figure and FuncAnimation to animate it.
		The show function returns the animation object.
		
		:return: An animation object
		"""
		if self.solution is None:
			self.solve()

		# 1. initialize the figure
		figure, axes = plt.subplots(1, 1, figsize=(12, 9))

		# 2. animate function
		def animate(i):
			axes.cla()  # we clear everything on the axe (there no way to just set data with imshow)

			# we get the solution of each equation at time i
			_, _, P0, P1, P2 = np.split(self.solution.y[:, i].reshape(self.shape * 5, self.shape), 5)

			axes.imshow(Model.get_pigment_matrix(P0, P1, P2), vmin=0, vmax=3, cmap=ListedColormap(
				['w', 'tan', 'black', 'yellow']))  # use vmin and vmax to avoid legend (color) change.
			axes.set_title(f'Evolution until time {self.solution.t[i]:.2f}')

			return axes

		# 3. call the animator
		return FuncAnimation(figure, animate, frames=self.solution.t.size, interval=30)
