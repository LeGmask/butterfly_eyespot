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

		# numpy as row and column inverted, so we need to invert data from request
		A0_pos = [[pos[1], pos[0]] for pos in request.json['A0_pos']]

		model = Model(shape=request.json['grid_size'])
		model.append_A0_pos(A0_pos)

		print(request.json['A0_pos'])

		model.solve()

		# M1, M2, P0, P1, P2 = model.restore_dimension(model.solution.y[:, -1])
		#
		# return {
		# 	'M1': M1.tolist(),
		# 	'M2': M2.tolist(),
		# 	'P0': P0.tolist(),
		# 	'P1': P1.tolist(),
		# 	'P2': P2.tolist(),
		# }
		return model.solution.y.tolist()
	else:
		return 'Content-Type not supported!'


if __name__ == "__main__":
	app.run(debug=True)
