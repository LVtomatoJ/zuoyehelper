<template>
  <template v-if="timeout">
    <div style="text-align: center;">
      <h2>
        收集已过期
      </h2>
    </div>
  </template>
  <template v-else>
    <Card  :padding="0" shadow style="width: auto;">
      <template #title>
              {{ props.collect_data.title }} （{{props.collect_data.destict}}）
            </template>
      <CellGroup style="padding-top: 10px;">
        <template v-for="item in props.collect_data.need">
          <Cell :title="item.name">
            <template #extra>
              <Input v-model="item.value" placeholder="" style="width: auto" />
            </template>
          </Cell>
        </template>
      </CellGroup>

      <el-upload style="padding-top: 10px;" method="put" class="upload-demo" drag :action="uploadurl" :before-upload="getUploadUrl">
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        拖住文件或 <em>点击此处上传</em>
      </div>
    </el-upload>
    </Card>
    



  </template>
</template>

<script setup>
import { UploadFilled } from '@element-plus/icons-vue'
import { service } from '../../stores/axios.js'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {ref} from 'vue'
const route = useRoute();
const collect_id = route.params.collect_id
const props = defineProps(['collect_data'])
let timeout = new Date(props.collect_data.endtime) < new Date()
let filename = ''
let uploadurl = ref('')
console.log(props.collect_data)

//获取上传地址
function getUploadUrl(rawFile) {
  filename = rawFile.name
  //判空
  for (let index = 0; index < props.collect_data.need.length; index++) {
    const element = props.collect_data.need[index];
    if ((!element['value'])||element['value']===''){
      ElMessage.error('请填写全部内容后上传文件')
      return false
    }
  }
  return service({ method: 'post', params: { collect_id: collect_id }, url: '/public/upload', data: { data: props.collect_data.need, filename: filename } }).then(res => {
    const data = res.data
    if (data.code === 200) {
      uploadurl.value = data.message
    } else {
      ElMessage.error('上传失败,' + 'code: ' + data.code + ' | message: ' + data.message)
      return false
    }
  }).catch((error) => {
    ElMessage.error('请求失败')
    return false
  })
}
</script>