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
    </div>
</template>
<script>
import { useLoginStore } from '../stores/login'

export default {
    data() {
        return {
            autoLogin: true
        }
    },
    methods: {
        handleSubmit(valid, { username, password }) {
            const store = useLoginStore()
            if (valid) {
                let formData = new FormData();
                formData.append("username", username);
                formData.append("password", password);
                fetch('http://127.0.0.1:8000/token', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.code == 200) {
                            this.$Modal.info({
                                title: '成功',
                                content: '登录成功'
                            });
                            console.log(data)
                            store.isLoggedIn = true
                            store.jwt = data.access_token
                        } else {
                            this.$Modal.info({
                                title: '错误',
                                content: 'code: ' + data.code + ' | message: ' + data.message
                            });
                        }
                    });

                // this.$Modal.info({
                //     title: '输入的内容如下：',
                //     content: 'username: ' + username + ' | password: ' + password
                // });
            }
        }
    }
}
</script>
<style>
.demo-login {
    width: 400px;
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
