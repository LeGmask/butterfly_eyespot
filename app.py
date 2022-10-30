from flask import Flask, send_from_directory, request
from flask_cors import CORS

from src.model import Model

app = Flask(__name__)
CORS(app)


#  Serve Svelte SPA
@app.route("/")
def base():
	return send_from_directory('dist', 'index.html')


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
	return send_from_directory('dist', path)


@app.route("/run", methods=['POST'])
def run_simulation():
	content_type = request.headers.get('Content-Type')
	if content_type == 'application/json':
		print(request.json)

		# numpy as row and column inverted, so we need to invert data from request
		A0_pos = [(pos[1], pos[0]) for pos in request.json['A0_pos']]

		model = Model(
			grid_size=request.json['grid_size'],
			time_span=(request.json['time_span'][0], request.json['time_span'][1]),
			time_step=request.json['time_step'],
			k1=request.json['k1'],
			k2=request.json['k2'],
			k3=request.json['k3'],
			k4=request.json['k4'],
			k5=request.json['k5'],
			D1=request.json['D1'],
			D2=request.json['D2'],
			M1_0=request.json['M1_0'],
			M2_0=request.json['M2_0'],
			P0_0=request.json['P0_0'],
			P1_0=request.json['P1_0'],
			P2_0=request.json['P2_0'],
			A_0=request.json['A_0'],
			P0_0_with_precursor=request.json['P0_0_with_precursor'],
			A0_0_with_precursor=request.json['A0_0_with_precursor']
		)

		model.append_A0_pos(A0_pos)
		model.solve()

		M1, M2, P0, P1, P2 = model.restore_dimension(model.solution.y[:, -1])

		return {
			'M1': M1.tolist(),
			'M2': M2.tolist(),
			'P0': P0.tolist(),
			'P1': P1.tolist(),
			'P2': P2.tolist(),
		}
		# return model.solution.y.tolist()
	else:
		return 'Content-Type not supported!'


if __name__ == "__main__":
	app.run(debug=True)
