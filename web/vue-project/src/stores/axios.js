import axios from 'axios'
export const service = axios.create({
	baseURL: API_URI+'/api'
})