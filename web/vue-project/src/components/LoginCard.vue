<template>
    <div class="demo-login">
        <Login @on-submit="handleSubmit">
            <UserName name="username" />
            <Password name="password" />
            <div class="demo-auto-login">
                <Checkbox v-model="autoLogin" size="large">自动登录</Checkbox>
                <a>忘记密码</a>
            </div>
            <Submit />
        </Login>
        <Button @click="goReg" size="large" style="padding-top: 5px;" long>注册</Button>
    </div>
    
</template>
<script>
import { useLoginStore } from '../stores/login'
import axios from 'axios'

export default {
    data() {
        return {
            autoLogin: true
        }
    },
    methods: {
        //登录操作
        handleSubmit(valid, { username, password }) {
            const store = useLoginStore()
            if (valid) {
                axios.post(API_URI+'/token', {
                    'username': username,
                    'password': password
                }, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then(res => {
                    const data = res.data
                    if (data.code === 200) {
                        this.$Message.success('登录成功,即将跳转主页');
                        store.isLoggedIn=true
                        store.jwt=data.access_token
                        this.$router.push('/')
                        
                    } else {
                        this.$Message.error('登录失败,' + 'code: ' + data.code + ' | message: ' + data.message);
                    }
                }).catch(function (error) {
                    this.$Message.error('网络请求失败')
                })
            }
        },
        goReg(){
            this.$router.push({'name':'reg'})
        }
    }
}
</script>
<style>
.demo-login {
    width: auto;
    max-width: 400px;
    margin: 0 auto !important;
}

.demo-auto-login {
    margin-bottom: 24px;
    text-align: left;
}

.demo-auto-login a {
    float: right;
}
</style>
