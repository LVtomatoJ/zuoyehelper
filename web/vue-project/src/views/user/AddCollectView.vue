<template>
    <template v-if="type.value === '0'">

        <div style="position: relative;height: 100px;padding-top: 30px;">

            <Card title="单文件收集" icon="ios-options" :padding="0" shadow style="padding-top: 30px;,width: auto;min-width: 300px;position: absolute;
      left: 50%;transform: translateX(-50%);">
                <CellGroup>
                    <Divider>收集表编辑</Divider>
                    <Cell title="标题">
                        <template #extra>
                            <Input v-model="title" />
                        </template>
                    </Cell>
                    <Cell title="描述">
                        <template #extra>
                            <Input v-model="destict" />
                        </template>
                    </Cell>
                    <Divider>结束时间</Divider>
                    <DatePicker v-model:model-value="endtime" style="width: 100%;" type="datetime" placeholder="" />
                    <Divider>需求（自动重命名文件）</Divider>
                    <Cell title="序号">
                        <template #extra>
                            名称
                        </template>
                    </Cell>
                    <template v-for="item in need">
                        <Cell :title="item.index">
                            <template #extra>
                                <Input v-model="item.name" />
                            </template>
                        </Cell>
                    </template>
                    <Button  @click="addNeed" long>添加需求</Button>
                </CellGroup>
                <Divider />
                <Button long @click="onAddCollect" type="success">上传收集表</Button>
            </Card>
        </div>
        <Modal v-model="modal_show" title="表单创建成功" @on-ok="ok" @on-cancel="cancel">
            <p>标题:{{ title }}</p>
            <p>结束时间:{{ endtime }}</p>
            上传地址:<Input class="btn" v-model="upload_url" @click="copyurl" readonly/>
            
            
        </Modal>
    </template>
    <template v-else>
        暂无
    </template>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { service } from '../../stores/axios.js'
import { ref } from 'vue'
import useClipboard from 'vue-clipboard3'
const { toClipboard } = useClipboard()

//获取类型
const route = useRoute();
let need = ref([])
let type = ref('')
let modal_show = ref(false)
let title = ''
let destict = ''
let upload_url = ref('')
let endtime = new Date()
type.value = ref(route.params.type)


const copyurl = async () => {
      try {
        await toClipboard(upload_url.value)
        ElMessage.success('链接复制成功')
      } catch (e) {
        ElMessage.error('链接复制失败')
      }
    }


function addNeed() {
    const lens = need.value.length
    console.log(lens)
    need.value.push({ 'index': lens + 1, 'name': '' })
}
function onAddCollect() {
    if (title == '' || destict == '') {
        ElMessage.error('请填写标题和描述')
    } else {

        for (let index = 0; index < need.value.length; index++) {
            const element = need.value[index];
            if (element['name'] === '') {
                ElMessage.error('请填写需求名称')
                return
            }
        }
        service({
            method: 'post',
            url: '/collect/add',
            data: {
                endtime: endtime.toLocaleString,
                type: route.params.type,
                title: title,
                destict: destict,
                need: need.value
            }
        }).then(res => {
            const data = res.data
            if (data.code === 200) {
                upload_url.value = data.message
                modal_show.value = true
            } else {
                ElMessage.error('上传失败,' + 'code: ' + data.code + ' | message: ' + data.message)
                return false
            }
        }).catch((error) => {
            ElMessage.error('请求失败')
            return false
        })
    }
}
</script>