<template>
    <div style="padding-top: 40px;">
        <Row>
            <Col span="2">
            </Col>
            <Col span="20">
            <Grid center square :border="false" :hover="true">
                <GridItem @click="goAddCollectPage(0)">
                    单文件收集
                </GridItem>
            </Grid>
            </Col>
            <Col span="2">
            </Col>
        </Row>
    </div>
</template>

<script setup>
import {  useRouter } from 'vue-router'
const router = useRouter();

function goAddCollectPage(type){
    router.push('/user/addcollect/'+type)
}
</script>