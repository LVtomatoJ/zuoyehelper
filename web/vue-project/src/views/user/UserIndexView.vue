<template>
    <template v-if="mobile_flag">
        <div class="head" style="padding-top: 20px;padding-left: 20px;">
            <h2>作业帮收件箱</h2>
        </div>
        <div class="menu">

            <Menu class="el-menu-demo" mode="horizontal" @on-select="change_menu" :active-name="menu_active"
                style="margin-top: 20px">
                <MenuItem name="创建收集">
                <Icon type="md-document" />
                创建收集
                </MenuItem>
                <MenuItem name="收集列表">
                <Icon type="md-chatbubbles" />
                收集列表
                </MenuItem>

            </Menu>
            <div class="content">
                    <template v-if="menu_active === '创建收集'">
                        <AddCollectList>
                        </AddCollectList>
                    </template>
                    <template v-else-if="menu_active == '收集列表'">
                        <div>
                            <GetCollectList>
                            </GetCollectList>
                        </div>
                    </template>
                    <template v-else>
                        待实现...
                    </template>
                </div>
        </div>

    </template>
    <template v-else>
        <div>
            <Row align="top">
                <Col flex="none">
                <div style="height:100vh">
                    <row style="margin-top:10px;margin-left: 20px;">
                        <h2>作业帮收件箱</h2>
                    </row>
                    <Menu @on-select="change_menu" width="auto" :active-name="menu_active"
                        style="margin-top: 20px;height:100%">
                        <MenuGroup title="收集管理">
                            <MenuItem name="创建收集">
                            <Icon type="md-document" />
                            创建收集
                            </MenuItem>
                            <MenuItem name="收集列表">
                            <Icon type="md-chatbubbles" />
                            收集列表
                            </MenuItem>
                        </MenuGroup>
                        <MenuGroup title="统计分析">
                            <MenuItem name="3">
                            <Icon type="md-heart" />
                            用户留存
                            </MenuItem>
                            <MenuItem name="4">
                            <Icon type="md-leaf" />
                            流失用户
                            </MenuItem>
                        </MenuGroup>
                    </Menu>
                </div>

                </Col>
                <Col flex="auto">
                <div>
                    <template v-if="menu_active === '创建收集'">
                        <AddCollectList>
                        </AddCollectList>
                    </template>
                    <template v-else-if="menu_active == '收集列表'">
                        <div>

                            <GetCollectList>
                            </GetCollectList>
                        </div>
                    </template>
                    <template v-else>
                        待实现...
                    </template>
                </div>

                </Col>
            </Row>
        </div>
    </template>
</template>
<script setup>
import AddCollectList from '../../components/user/AddCollectList.vue'
import GetCollectList from '../../components/user/GetCollectList.vue'
import { ref } from 'vue'
let menu_active = ref('创建收集')
function change_menu(name) {
    menu_active.value = name
}

var screen_width = window.screen.width;
var screen_height = window.screen.height;
console.log(screen_height)
console.log(screen_width)
let mobile_flag = false
//根据屏幕分辨率判断是否是手机
if (screen_width > 325 && screen_height < 750) {
    mobile_flag = true;
}

</script>