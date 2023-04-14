<template>
    <div>
        <div style="display: flex;padding-top: 10px;padding-bottom: 10px;">
            <Page style=" margin: auto" :total="total" @on-change="changePage" />
        </div>
        <el-table :data="listdata" style="width: auto" table-layout="auto">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="destict" label="描述" />
            <el-table-column prop="status" label="状态" />
            <el-table-column label="操作">
                <template #default="scope">
                    <template v-if="scope.row.status === '已结束'">
                        <el-button size="small" type="success"
                            @click="handleDownload(scope.$index, scope.row)">下载文件</el-button>
                    </template>
                    <template v-else>
                        <el-button size="small" type="danger" @click="handleStop(scope.$index, scope.row)">停止收集</el-button>
                    </template>
                    <!-- <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button> -->
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
<script setup>
import { service } from '../../stores/axios.js'
import { ref, onMounted } from 'vue'
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

function handleStop(index, row) {
    const collect_id = row['_id']
    console.log(collect_id)
}
function handleDownload(index, row) {
    const collect_id = row['_id']
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