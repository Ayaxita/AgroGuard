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
        <el-button type="danger" :icon="Delete" @click="deleteData(scope.selectedListIds)">删除</el-button>
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
    <GrassDrawer ref="drawerRef" />
    <ImportExcel ref="dialogRef" />
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { User } from "@/api/interface";
import { ElMessage, ElMessageBox } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import GrassDrawer from "../components/GrassDrawer.vue";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import { getManuList, editManu, addManu, delManu, exportGrassInfo } from "../api/manu";
import {
  fieldTransferReasonType,
  d_plantcareDetection_modeType,
  d_plantcareResult1Type,
  d_plantcareResult2Type,
  d_plantcareResult3Type,
  d_plantcareSituationType,
  Feeding_wayType,
  manuScaleType,
  manutypeType,
  HardeningRankType
} from "@/assets/json/typeListJson";
import { useDownload } from "@/hooks/useDownload";

const router = useRouter();

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
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  // {
  //   prop: "lamb_id",
  //   label: "批次id",
  //   search: {
  //     el: "input",
  //     props: {
  //       type: "number"
  //     }
  //   }
  // },
  {
    prop: "logo",
    label: "批次标识",
    width: 250,
    search: {
      el: "input"
    }
  },
  {
    prop: "lamb_ele_num",
    label: "草地编号",
    width: 200,
    search: {
      el: "input"
    }
  },
  {
    prop: "lamb_pre_num",
    label: "地块编号",
    search: {
      el: "input"
    }
  },
  {
    prop: "Delivery_date",
    label: "阶段切换日期",
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
    prop: "feeding_way",
    label: "管理方式",
    enum: Feeding_wayType,
    fieldNames: {
      label: "label",
      value: "value"
    },
    search: {
      el: "select"
    }
  },
  {
    prop: "Bir_weight",
    label: "初始生物量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "wea_weight",
    label: "阶段末生物量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "rank",
    label: "阶段评级",
    enum: HardeningRankType,
    fieldNames: {
      label: "label",
      value: "value"
    },
    search: {
      el: "select"
    }
  },
  { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};
//todo
//删除
const deleteData = datasinfo => {
  if (datasinfo.length !== 0) {
    ElMessageBox.confirm(`确认删除信息?<br/>已选${datasinfo.length}条数据`, "温馨提示", {
      type: "warning",
      dangerouslyUseHTMLString: true
    }).then(() => {
      //通过这个函数把所选数据id传到后端
      delManu(datasinfo).then(res => {
        if (res.code === 200) {
          ElMessage.success("删除成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        } else {
          ElMessage.error("删除出错！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要删除的信息！");
  }
};
// const deleteData = () => {
//   console.log(proTable.value?.tableData);
//   ElMessage.success("修改列表排序成功");
// };
// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportGrassInfo, "阶段切换信息导出结果", proTable.value?.searchParam)
  );
};
//导出所选数据
const downloadSelectFile = async selectedListIds => {
  // 获取用户在表格中所选的记录数据
  const selectedGrassData = selectedListIds;

  if (!selectedGrassData || selectedGrassData.length === 0) {
    ElMessage.warning("请先选择要导出的数据！");
    return;
  }

  ElMessageBox.confirm(`确认导出所选的${selectedGrassData.length}条数据?`, "温馨提示", { type: "warning" }).then(() => {
    // 调用useDownload函数进行导出，并传入所选记录数据、导出文件名以及其他可能需要的参数（这里假设暂时不需要其他参数）
    useDownload(() => exportGrassInfo(selectedGrassData), `阶段切换信息导出结果`, null);
  });
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
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
</script>
