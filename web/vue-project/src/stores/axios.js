import axios from 'axios'
import { useLoginStore } from '../stores/login'
import { ElMessage } from 'element-plus'

const service = axios.create({
	baseURL: API_URI+'/api'
})

service.interceptors.request.use(function (config) {
	const store = useLoginStore()
	if (store.isLoggedIn){
		config.headers.setAuthorization('Bearer '+store.jwt)
	}
    return config;
  }, function (error) {
    return Promise.reject(error);
  });

  service.interceptors.response.use(function (response) {
    return response;
  }, function (error) {
	if(error.response.statusText==="Unauthorized"){
		const store = useLoginStore()
		store.jwt='',
		store.isLoggedIn=false
		ElMessage.error('登录过期,请重新登录')
	}
	
    return Promise.reject(error);
  });

export {service}