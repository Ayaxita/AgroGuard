<template>
  <div class="table-box">
    <ProTable
      ref="proTable_test"
      :columns="columns"
      :request-api="getTableList"
      :data-callback="dataCallback"
      @drag-sort="sortTable"
      :search-col="4"
    >
      <!-- 表格 header 按钮 -->
      <template #tableHeader="">
        <el-button type="primary" :icon="CirclePlus" @click="openDialog(true)">阈值设置</el-button>
        <el-button type="primary" :icon="CirclePlus" @click="updateWarnmessage()" :disabled="isButtonDisabled">
          更新草地防护预警信息
        </el-button>
        <!-- <el-button type="primary" :icon="CirclePlus" @click="SmallRuminantVaccine"> 植保药剂 </el-button>
        <el-button type="primary" :icon="CirclePlus" @click="openDialog(true)">真菌病防护剂</el-button>
        <el-button type="primary" :icon="CirclePlus" @click="openDialog(true)">锈病防护剂</el-button>
        <el-button type="primary" :icon="CirclePlus" @click="openDialog(true)">综合防护剂</el-button> -->
        <!-- <el-button type="danger" :icon="Delete" @click="deleteData(scope.selectedList)">删除</el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadFile(scope.selectedList)">导出所选数据</el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadFile([])">导出所有数据</el-button> -->
      </template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
      <!-- 表格操作 -->
      <template #operation="">
        <!-- <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button>
        <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)">编辑</el-button> -->
      </template>
    </ProTable>
    <thresholdSet ref="dialogRef" />
    <SheepDrawer ref="drawerRef" />
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive, onMounted, watch, inject, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import { User } from "@/api/interface";
import { ElMessage, ElMessageBox } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import SheepDrawer from "../components/SheepDrawer.vue";
import { ProTableInstance, ColumnProps, HeaderRenderScope } from "@/components/ProTable/interface";
import { CirclePlus, Delete, Download, EditPen, MessageBox, SetUp, View } from "@element-plus/icons-vue";
import { editThresholdeinfo, getManuList, getThresholdeinfo, updateWarnMessage } from "../api/manu";
import { colonyTransferReasonType, manuScaleType, manutypeType, sexType } from "@/assets/json/typeListJson";
import { useDownload } from "@/hooks/useDownload";
import thresholdSet from "../components/thresholdSet.vue";
import { useTable } from "@/hooks/useTable";
import { useTempStore } from "@/stores/modules/apiStore";

// ProTable 实例
const proTable = ref<ProTableInstance>();
const useTable1 = useTable();
const tempstore = useTempStore();
const isButtonDisabled = ref(false); // 按钮是否禁用
isButtonDisabled.value = JSON.parse(localStorage.getItem("isbuttondisabled") || "null");

// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};

//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  console.log("进入这里了");
  let newParams;
  if (tempstore.Data) {
    params = tempstore.Data;
    tempstore.updateMessageInfo(null);
  }
  newParams = JSON.parse(JSON.stringify(params));
  // if (warnMessagetransport) newParams = JSON.parse(JSON.stringify(params));
  // else newParams = newParams = { ...params, ...warnMessagetransport };
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  return getManuList(newParams);
};

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  /*{ type: "sort", label: "Sort", width: 80 },
  
  {
    prop: "basic_id",
    label: "草地基本信息",
    search: {
      el: "input"
    }
  },*/
  { type: "expand", label: "Expand", width: 85 },
  {
    prop: "ele_num",
    label: "草地编号",
    search: {
      el: "input"
    }
  },
  {
    prop: "pre_num",
    label: "地块编号",
    search: {
      el: "input"
    }
  },
  {
    prop: "sex",
    label: "作物类型",
    enum: sexType,
    search: {
      el: "input"
    }
  },
  {
    prop: "mon_age",
    label: "生长月数",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "cname",
    label: "防护剂名称",
    search: {
      el: "input"
    }
  },
  {
    prop: "imm_date",
    label: "上次防护日期",
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  },
  {
    prop: "house",
    label: "所在站点",
    search: {
      el: "input"
    }
  },
  {
    prop: "hurdle_name",
    label: "所在地块",
    search: {
      el: "input"
    }
  },
  {
    prop: "dead_date",
    label: "截至日期",
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  }
  // ,
  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);

const updateWarnmessage = async () => {
  ElMessageBox.confirm(
    "此操作会根据当前日期更新草地防护预警信息，逻辑复杂，耗时较多（大约十五分钟），请在空闲时操作，你确认要现在更新吗？",
    "温馨提示",
    { type: "warning" }
  )
    .then(() => {
      updateWarnMessage(); //isButtonDisabled.value = true;
      //computedTime();
    })
    .finally(() => {
      window.location.reload();
    });
};

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};
const dialogRef = ref<InstanceType<typeof thresholdSet> | null>(null);
const openDialog = async (isOpen: boolean) => {
  if (isOpen) {
    try {
      const response = await getThresholdeinfo(); // 请求后端数据
      if (Array.isArray(response.data.list)) {
        console.log("后端返回数据：", response.data);
        const dialogProps = {
          isView: isOpen,
          model_data: response.data.list,
          api: editThresholdeinfo,
          getTableList: proTable.value?.getTableList
        };
        // 调用子组件的 acceptParams 方法，并传递后端数据
        dialogRef.value?.acceptParams(isOpen, dialogProps);
      }
    } catch (error) {
      console.error("获取阈值信息失败：", error);
    }
  }
};

defineExpose({
  getTableList
});
// let warnMessagetransport;
// const SmallRuminantVaccine = () => {
//   warnMessagetransport = {
//     pageNum: 1,
//     pageSize: 10,
//     vaccine_id: 9
//     // 其他需要的搜索条件
//   };
//   console.log(warnMessagetransport);
//   getTableList(warnMessagetransport);
// };
//todo
//删除免疫信息
// const deleteData = async delinfo => {
//   console.log("选中的删除信息", delinfo);
//   if (delinfo.length !== 0) {
//     ElMessageBox.confirm(`确认删除对象?<br/>已选${delinfo.length}只羊`, "温馨提示", {
//       type: "warning",
//       dangerouslyUseHTMLString: true
//     }).then(() => {
//       delImmunizationinfo(delinfo).then(res => {
//         if (res === 200) {
//           ElMessage.success("删除成功！");
//           proTable.value?.clearSelection();
//           proTable.value?.getTableList();
//         } else {
//           ElMessage.error("删除免疫信息出错！");
//         }
//       });
//     });
//   } else {
//     ElMessage.warning("请先选择要标记的草地！");
//   }
// };

// 导出列表
// const downloadFile = async selectlist => {
//   if (selectlist.length !== 0) {
//     console.log("选中的信息", selectlist);
//     ElMessageBox.confirm("确认导出所选数据?", "温馨提示", { type: "warning" }).then(() =>
//       useDownload(() => exportImmunizationInfo(selectlist), "草地防护信息导出结果")
//     );
//     proTable.value?.clearSelection();
//   } else {
//     ElMessageBox.confirm("确认导出全部数据?", "温馨提示", { type: "warning" }).then(() =>
//       useDownload(() => exportImmunizationInfo(selectlist), "草地防护信息导出结果")
//     );
//   }
// };
// 打开 drawer(新增、查看、编辑)
// const drawerRef = ref<InstanceType<typeof SheepDrawer> | null>(null);
// const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
//   const params = {
//     title,
//     isView: title === "查看",
//     row: { ...row },
//     api: title === "新增" ? addManu : title === "编辑" ? editManu : undefined,
//     getTableList: proTable.value?.getTableList
//   };
//   console.log(params);
//   drawerRef.value?.acceptParams(params);
// };
function computedTime() {
  new Date();
}
</script>
