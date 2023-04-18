# zuoyehelper 作业帮（bushi
帮助大学生收集各种文件的系统(未完成)
# 技术栈
## fastapi(后端
## vite(生成前端单页面
# 使用
## 后端
### 构建python虚拟环境（venv）
```
python3 -m venv venv
source venv/bin/activate
```
### 安装 web/requirements.txt中所包含的库
```
python3 -m pip install -r requirements.txt

另外
因为腾讯官方sdk中没有部分接口所以fork了之后自己完成了需要的部分接口 需要自行下载安装哦！
```
### 安装mongodb
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

### 启动服务（在web目录下）
```
python3 -m uvicorn fastapi-project.main:app --reload
python3 -m uvicorn fastapi-project.main:app --host='0.0.0.0'
````
## 前端
### 安装node以及所需库
npm install
### 启动服务
```
npm run dev
```
