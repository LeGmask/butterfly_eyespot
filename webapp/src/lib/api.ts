import axios from "axios";

export const api = axios.create({
	baseURL: "http://localhost:5000",
	timeout: 300000, // 5 minutes since the server can take a while to respond if grid is large
	headers: {
		"Content-Type": "application/json",

	}
});