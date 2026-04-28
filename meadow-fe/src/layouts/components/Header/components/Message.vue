<template>
  <div class="message">
    <el-popover placement="bottom" :width="310" trigger="click">
      <template #reference>
        <el-badge :value="warnMessageslist.length" :hidden="warnMessageslist.length === 0" class="item">
          <i :class="'iconfont icon-xiaoxi'" class="toolBar-icon"></i>
        </el-badge>
      </template>
      <el-tabs v-model="activeName">
        <el-tab-pane label="通知(0)" name="first">
          <div class="message-empty">
            <img src="@/assets/images/notData.png" alt="notData" />
            <div>暂无消息</div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="消息(0)" name="second">
          <div class="message-empty">
            <img src="@/assets/images/notData.png" alt="notData" />
            <div>暂无消息</div>
          </div>
        </el-tab-pane>
        <el-tab-pane :label="`待办(${warnMessageslist.length})`" name="third">
          <div class="message-list">
            <!-- <div class="message-item">
              <img src="@/assets/images/msg01.png" alt="" class="message-icon" />
              <div class="message-content">
                <span class="message-title">预警信息 💜</span>
                <span class="message-date">共由 {{ warnMessageslist.length }} 条预警信息需要处理</span>
                <el-button class="message-commmit" type="text" @click="viewWarnMessage">查看详情</el-button>
              </div>
            </div> -->
            <div class="message-item" v-for="(message, index) in warnMessageslist" :key="index">
              <img src="@/assets/images/msg01.png" alt="" class="message-icon" />
              <div class="message-content">
                <span class="message-title">关于 {{ message.cname }} 的预警信息 💜</span>
                <span class="message-date" v-if="message.note">防治病虫害描述：{{ message.note }}</span>
                <span class="message-date">共由 {{ message.Messagelength }} 条预警信息需要处理</span>
                <el-button class="message-commmit" type="text" @click="viewWarnMessage(message.vaccine_id)"> 查看详情 </el-button>
              </div>
            </div>
            <div v-if="warnMessageslist.length === 0" class="message-empty">
              <img src="@/assets/images/notData.png" alt="notData" />
              <div>暂无待办</div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { provide, reactive, ref } from "vue";
import { useAuthStore } from "@/stores/modules/auth";
import { useRoute, useRouter } from "vue-router";
import { useTempStore } from "@/stores/modules/apiStore";
import { useTable } from "@/hooks/useTable";
import getTableList from "@/views/w_information/immunizationMessage/useProTable/index.vue";
import { ElMessageBox } from "element-plus";

// const gettableList = ref(null);
// const xxx = ref();
const router = useRouter();
const route = useRoute();
const activeName = ref("first");
const tempstore = useTempStore();
// const warnMessages = reactive([
//   { ele_num: "131102202240632", house: "A区", hurdle_name: "1栏", message: "防犬防护措施 未接种", deadline: "2024-12-12" },
//   { ele_num: "131102202401659", house: "A区", hurdle_name: "1栏", message: "防犬防护措施 未接种", deadline: "2024-12-12" }
// ]);
const warnMessageslist = useAuthStore().authMessageListLength;
//console.log("warnMessages", warnMessageslist);
let warnMessagetransport;

const viewWarnMessage = params => {
  // gettableList.value.getTableList;
  // console.log(xxx);
  // console.log(gettableList);
  // if (gettableList.value && gettableList.value.getTableList) {
  //   // 调用子组件方法
  //   gettableList.value.getTableList({ page: 1, pageSize: 10 });
  // } else {
  //   console.error("无法获取子组件实例或方法！");
  // }
  const currentDate = new Date();
  const formattedDate = currentDate.toISOString().split("T")[0];
  //console.log(formattedDate); // 输出: 2024-12-17
  warnMessagetransport = {
    pageNum: 1,
    pageSize: 10,
    vaccine_id: params,
    dead_date: ["2010-01-01", formattedDate]
    // 其他需要的搜索条件
  };

  tempstore.Data = warnMessagetransport;
  tempstore.updateMessageInfo(warnMessagetransport);
  console.log("搜索条件", warnMessagetransport);
  if (route.name != "w_information_immunizationMessage") {
    ElMessageBox.alert("刷新后的结果是筛选后的结果。").then(() => {
      router.push({
        name: "w_information_immunizationMessage"
      });
    });
  } else {
    console.log("当下的路由信息", route.fullPath, route.name);
    ElMessageBox.alert("刷新后的结果是筛选后的结果。").then(() => {
      window.location.reload();
    });

    // router
    //   .replace({
    //     name: "home"
    //   })
    //   .then(() => {
    //     router.push({
    //       name: "w_information_immunizationMessage"
    //     });
    //   });
    //getManuList(warnMessagetransport);id-3b098520-32a9-47d8-add9-732f9b617317
  }
};
</script>

<style scoped lang="scss">
.message-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 260px;
  line-height: 45px;
}
.message-list {
  display: flex;
  flex-direction: column;
  .message-item {
    display: flex;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid var(--el-border-color-light);
    &:last-child {
      border: none;
    }
    .message-icon {
      width: 40px;
      height: 40px;
      margin: 0 20px 0 5px;
    }
    .message-content {
      display: flex;
      flex-direction: column;
      .message-title {
        margin-bottom: 5px;
      }
      .message-commmit {
        display: flex;
        align-items: flex-end;
        justify-content: flex-end;
        text-decoration: underline;
      }
    }
  }
}
</style>
