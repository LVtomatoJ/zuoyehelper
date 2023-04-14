<script setup>
import { useRouter } from 'vue-router';
import { useLoginStore } from '../stores/login'
const store = useLoginStore()
const router = useRouter()


const handleLogin = () => { 
    router.push({path: '/login'})
 }

const handleLoginOut=()=>{
  store.isLoggedIn=false
  store.jwt=''
}

</script>

<template>
  <div class="'head'">
    <Row align="middle" style="margin-top: 20px;">
      <Col span="10">
      <div style="font-size: 20px">
        <div style="padding-left: 30px;">作业帮收件箱</div>
      </div>
      </Col>
      <Col span="2">
      </Col>
      <Col span="12">
      <div style="float: right;">
        <template v-if="store.isLoggedIn">
          <div style="padding-right: 20px;">

                  <Button to="/user/index" type="success" >控制台</Button>
                  <Divider type="vertical" />

                  <Button @click="handleLoginOut" type="warning">退出</Button>

              
            
          </div>
        </template>
        <template v-else>

          <div style="padding-right: 30px;">
            <Button @click="handleLogin" type="primary">登录</Button>
          </div>
        </template>
      </div>
      </Col>
    </Row>
  </div>
  <div>
    <div style="padding-top: 40px;font-size: 20px;text-align: center;">

      <p>使用对象存储实现的文件收集系统</p>
      <p>待补充..</p>
    </div>
</div></template>

