<template>
    <el-card class="box-card" header="注册账号">
    <el-form
    ref="ruleFormRef"
    :model="ruleForm"
    status-icon
    :rules="rules"
    label-width="70px"
    label-position="left"
  >
  <el-form-item label="用户名" prop="username">
      <el-input v-model="ruleForm.username" type="text" autocomplete="off" />
    </el-form-item>
    <el-form-item label="密码" prop="pass">
      <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
    </el-form-item>
    <el-form-item label="确认密码" prop="checkPass">
      <el-input
        v-model="ruleForm.checkPass"
        type="password"
        autocomplete="off"
      />
    </el-form-item>
    <el-form-item label="手机号" prop="phonenumber">
      <el-input v-model="ruleForm.phonenumber" type="number" autocomplete="off" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)"
        >提交</el-button
      >
    </el-form-item>
  </el-form>
  </el-card>

</template>
<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
const ruleFormRef = ref()
import { useRouter } from 'vue-router'
const router = useRouter();

const validateUsername = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入用户名'))
  } else {
    callback()
  }
}
const validatePhonenumber = (rule, value, callback) => {
console.log(value)
  if (value === '') {
    callback(new Error('请输入手机号'))
  } else {

        callback()

  }
}

const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass', () => null)
    }
    callback()
  }
}
const validatePass2 = (rule, value, callback) => {
    
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== ruleForm.pass) {
    callback(new Error("两次密码不相同!"))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  pass: '',
  checkPass: '',
  username:'',
  phonenumber:null,
})

const rules = reactive({
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  username:[{validator:validateUsername,trigger:'blur'}],
  phonenumber:[{validator:validatePhonenumber,trigger:'blur'}]
})
function submitReg(){
    axios({
        method:'post',
        url:API_URI+'/reg',
        data:{
            'password':ruleForm.pass,
            'username':ruleForm.username,
            'phonenumber':ruleForm.phonenumber,
        }
    }).then(res=>{
        let data =res.data
        if (data.code === 200) {
            ElMessage.success('注册成功,即将跳转登录页面');
            router.push('/login')
            } else {
                ElMessage.error('注册失败,' + 'code: ' + data.code + ' | message: ' + data.message)
                return false
        }
    })
}

const submitForm = (formEl) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      submitReg()
    } else {
      return false
    }
  })
}


</script>
<style></style>
