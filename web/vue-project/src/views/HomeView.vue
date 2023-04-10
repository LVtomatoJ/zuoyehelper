<script setup>
import { useRouter } from 'vue-router';
const router = useRouter()


const handleLogin = () => { 
    router.push({path: '/login'})
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
      <Col span="10">
      </Col>
      <Col span="4">
      <div style="float: right;">
        <div style="padding-right: 30px;">
          <Button @click="handleLogin" type="primary">登录</Button>
        </div>
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

