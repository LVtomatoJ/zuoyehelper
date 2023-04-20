<template>
    <div>
        <div style="display: flex;padding-top: 10px;padding-bottom: 10px;">
            <Page style=" margin: auto" :total="total" @on-change="changePage" />
        </div>
        <el-table :data="listdata" border style="width: 100%" table-layout="auto">
            <el-table-column fixed prop="title" label="标题" />
            <el-table-column prop="destict" label="描述" />
            <el-table-column width="70" prop="status" label="状态" />
            <el-table-column width="200" label="操作">
                <template #default="scope">
                    <template v-if="scope.row.status === '已结束'">
                        <el-button size="small" type="success"
                            @click="handleDownload(scope.$index, scope.row)">下载</el-button>
                            <el-button size="small" type="info"
                            @click="goUploadList(scope.$index, scope.row)">记录</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="danger" @click="handleStop(scope.$index, scope.row)">停止</el-button>
                        <el-button size="small" type="success" @click="copyUrl(scope.$index, scope.row)">复制</el-button>
                        <el-button size="small" type="info" @click="goUpdateCollect(scope.$index, scope.row)">修改</el-button>
                    </template>
                    <!-- <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button> -->
                </template>
            </el-table-column>
        </el-table>
    </div>
    <Modal v-model="showurl" title="下载地址" @on-ok="ok" @on-cancel="cancel">
        <a :href="downloadurl">点击下载</a>
    </Modal>
</template>
<script setup>
import useClipboard from 'vue-clipboard3'
const { toClipboard } = useClipboard()
import { service } from '../../stores/axios.js'
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
const router = useRouter();
let downloadurl = ref('')
let showurl = ref(false)
const columns = [
    {
        title: '标题',
        key: 'title'
    },
    {
        title: '描述',
        key: 'destict'
    },
    {
        title: '状态',
        key: 'status'
    }
]
let data = ref([])
let total = ref(0)
let listdata = ref([])
const copy = async (url) => {
    try {
        await toClipboard(url)
        ElMessage.success('链接复制成功')
    } catch (e) {
        ElMessage.error('链接复制失败')
    }
}
function goUpdateCollect(index, row) {
    router.push('/user/updateCollect/' + row['_id'])
}
function goUploadList(index, row) {
    router.push('/user/uploadCollect/' + row['_id'])
}
function copyUrl(index, row) {
    const url = WEB_URL + '/public/collect/' + row['_id']
    copy(url)
}

function handleStop(index, row) {
    const collect_id = row['_id']
    service({
        method: 'get',
        url: '/collect/stop',
        params: { collect_id: collect_id }
    }).then(res => {
        data = res.data
        if (data.code != 200) {
            ElMessage.error('停止失败' + 'code: ' + data.code + ' | message: ' + data.message)
        } else {
            ElMessage.success('收集表停止成功')
            row['status'] = '已结束'
        }
    })
}
function handleDownload(index, row) {
    const collect_id = row['_id']
    //结束收集
    //检查压缩是否完成
    service({
        method: 'get',
        url: '/collect/check_zip_job',
        params: { collect_id: collect_id }
    }).then(res => {
        data = res.data
        if (data.code != 200) {
            ElMessage.error('获取压缩进度失败' + 'code: ' + data.code + ' | message: ' + data.message)
        } else {
            const process = data.message
            if (process != '100') {
                ElMessage.success('压缩进度：' + process + '%')
            } else {
                //获取下载url
                service({
                    method: 'get',
                    url: '/collect/get_zip',
                    params: { collect_id: collect_id }
                }).then(res => {
                    data = res.data
                    if (data.code != 200) {
                        ElMessage.error('获取下载地址失败' + 'code: ' + data.code + ' | message: ' + data.message)
                    } else {
                        downloadurl.value = data.message
                        showurl.value = true
                    }
                })
            }
            row['status'] = '已结束'
        }
    })
    console.log(collect_id)
}


function getCollectTotal() {
    service({
        method: 'get',
        url: '/collect/total',
    }).then(res => {
        total.value = res.data.message
        console.log(total.value)
    })
}
function getCollectList(page, limit) {
    let nowdate = new Date()
    service({
        method: 'get',
        url: '/collect/get',
        params: {
            page: page,
            limit: limit
        }
    }).then(res => {
        let d = res.data.message
        d.forEach(element => {
            if (nowdate > new Date(element['endtime'])) {
                element['status'] = '已结束'
            } else {
                element['status'] = '进行中'
            }
        });
        // console.log(d)
        listdata.value = d
        // console.log(data)
    })
}
function changePage(p) {
    getCollectList(p, 10)

}

onMounted(() => {
    getCollectTotal()
    getCollectList(1, 10)
})


</script>