# zuoyehelper 作业帮（bushi
帮助大学生收集各种文件的系统(未完成)
# 技术栈
### fastapi
### vite
### mongodb

# 构建
## 后端
### 构建python虚拟环境（venv）
```
python3 -m venv venv
source venv/bin/activate
```
### 安装 web/requirements.txt中所包含的库
```
python3 -m pip install -r requirements.txt
```
另外
因为腾讯官方sdk中没有部分接口所以fork了之后自己完成了需要的部分接口 需要自行下载安装哦！

### 安装mongodb
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
### 配置
所有配置均在config.py文件中，
QCOS开头的需要在腾讯云对象存储服务中获得

### 启动服务（在web目录下）
#### 本地测试：
```
python3 -m uvicorn fastapi-project.main:app --reload
```
#### 开放外网：
```
python3 -m uvicorn fastapi-project.main:app --host='0.0.0.0'
```
## 前端
### 安装node（18）
node安装参考:
https://nodejs.dev/en/learn/how-to-install-nodejs/
### 安装所需包（package.json所在文件夹）
```
npm install
```
### 修改配置
配置文件在vite.config.js中修改后端地址和前端地址即可
### 启动服务
```
npm run dev
```
### build(生成单文件应用)
```
npm run build
```

## web服务器
### nginx安装以及使用
https://nginx.org/en/linux_packages.html#Ubuntu
https://nginx.org/en/docs/beginners_guide.html
### nginx配置
```
cd /etc/nginx/conf.d
vim default.conf
```
写入以下配置
```
server {
    listen       80; #监听端口
    server_name  localhost;
    location / {
        root /home/ubuntu/zuoyehelper/web/vue-project/dist; #项目路径
        index index.html;
        try_files $uri $uri/ /index.html; #单文件组件
    }

```

