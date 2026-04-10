<template>
  <div class="table-box">
    <ProTable
      ref="proTable"
      :columns="columns"
      :request-api="getTableList"
      :data-callback="dataCallback"
      @drag-sort="sortTable"
      :search-col="4"
    >
      <!-- 表格 header 按钮 -->
      <template #tableHeader="scope">
        <el-button type="primary" :icon="CirclePlus" @click="openDrawer('新增')">新增</el-button>
        <!-- <el-button type="danger" :icon="Delete" @click="deleteData(scope.selectedList)">删除</el-button> -->
        <el-button type="primary" :icon="Download" plain @click="downloadSelectFile(scope.selectedListIds)">
          导出所选数据
        </el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadFile">导出所有数据</el-button>
      </template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
      <!-- 表格操作 -->
      <template #operation="scope">
        <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button>
        <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)">编辑</el-button>
      </template>
    </ProTable>
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
import { getManuList, addManu, editManu, exportDailyreport } from "../api/manu";
import { colonyTransferReasonType, manuScaleType, manutypeType, sexType, DailyreportType } from "@/assets/json/typeListJson";
import { useDownload } from "@/hooks/useDownload";
import { useTable } from "@/hooks/useTable";
import { useTempStore } from "@/stores/modules/apiStore";

// ProTable 实例
const proTable = ref<ProTableInstance>();

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
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  return getManuList(newParams);
};

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "operation", label: "操作", fixed: "left", width: 150 },
  /*{ type: "sort", label: "Sort", width: 80 },
  
  {
    prop: "basic_id",
    label: "草地基本信息",
    search: {
      el: "input"
    }
  },*/
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "date",
    label: "记录日期",
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
    prop: "direct",
    label: "直接费用",
    _children: [
      {
        prop: "buysheep_fees",
        label: "种苗购买费用"
      },
      {
        prop: "caoliao_fees",
        label: "草地投入费用"
      },
      {
        prop: "jingliao_fees",
        label: "精准投入费用"
      },
      {
        prop: "yimiao_fees",
        label: "防护费用"
      },
      {
        prop: "yaopin_fees",
        label: "药物费用"
      },
      // {
      //   prop: "food_fees",
      //   label: "饲料费用"
      // },
      // {
      //   prop: "drug_fees",
      //   label: "药品/疫苗费用"
      // },
      {
        prop: "test_fees",
        label: "监测检验费用"
      },
      {
        prop: "labor_fees",
        label: "人工费用"
      },
      {
        prop: "waterEle_fees",
        label: "水电费用"
      },
      {
        prop: "land_fees",
        label: "地租费用"
      },
      {
        prop: "maintenance_fees",
        label: "设备维修费用"
      }
      // {
      //   prop: "directtotal_fees",
      //   label: "直接费用总花费"
      // }
    ]
  },
  {
    prop: "indirect",
    label: "间接费用",
    _children: [
      {
        prop: "cheep_fees",
        label: "低值易耗品费用"
      },
      {
        prop: "manage_fees",
        label: "管理费用"
      },
      {
        prop: "research_fees",
        label: "研发费用"
      },
      {
        prop: "other_fees",
        label: "其他费用"
      },
      {
        prop: "other_text",
        label: "其他费用说明"
      }
      // {
      //   prop: "indirecttotal_fees",
      //   label: "间接费用总花费"
      // }
    ]
  },
  {
    prop: "f_date",
    label: "创建日期",
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
    prop: "f_staff",
    label: "创建人员",
    search: {
      el: "input"
    }
  }
  // ,
  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

defineExpose({
  getTableList
});

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
//     ElMessage.warning("请先选择要标记的羊只！");
//   }
// };
// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportDailyreport, "日支出报表导出结果", proTable.value?.searchParam)
  );
};
//导出所选数据
const downloadSelectFile = async selectedListIds => {
  // 获取用户在表格中所选的羊只数据
  const selectedSheepData = selectedListIds;

  if (!selectedSheepData || selectedSheepData.length === 0) {
    ElMessage.warning("请先选择要导出的草地记录数据！");
    return;
  }

  ElMessageBox.confirm(`确认导出所选的${selectedSheepData.length}条日支出报表数据?`, "温馨提示", { type: "warning" }).then(() => {
    // 调用useDownload函数进行导出，并传入所选羊只数据、导出文件名以及其他可能需要的参数（这里假设暂时不需要其他参数）
    useDownload(() => exportDailyreport(selectedSheepData), `日支出报表导出结果`, null);
  });
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof SheepDrawer> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    api: title === "新增" ? addManu : title === "编辑" ? editManu : undefined,
    getTableList: proTable.value?.getTableList
  };
  console.log(params);
  drawerRef.value?.acceptParams(params);
};
function computedTime() {
  new Date();
}
</script>
