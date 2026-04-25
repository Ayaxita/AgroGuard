<template>
  <div class="table-box">
    <ProTable ref="proTable" :columns="columns" :request-api="getTableList" :data-callback="dataCallback" :search-col="4">
      <!-- 表格 header 按钮 -->
      <template #tableHeader="scope">
        <el-button type="primary" :icon="Refresh" @click="updateData">更新草地资产</el-button>
        <!-- <el-button type="danger" :icon="Delete" @click="deleteData(scope.selectedListIds)">删除</el-button> -->
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
      <!-- <template #operation="scope"> -->
      <!-- <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button> -->
      <!-- <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)">编辑</el-button> -->
      <!-- </template> -->
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
import { CirclePlus, Delete, Download, EditPen, Refresh, View } from "@element-plus/icons-vue";
import { exportGrassInfo, getManuList, updateGrassAsset } from "../api/manu";
import {
  assetStandardType,
  BooleanType,
  colonyDisinfectionMethodType,
  manuScaleType,
  manutypeType,
  purposeType,
  sexType,
  varietyType
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
  // { prop: "operation", label: "操作", fixed: "left", width: 100 },
  {
    prop: "variety",
    label: "草地类型",
    // width: 90,
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "sex",
    label: "作物类型",
    enum: sexType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "purpose",
    label: "类别",
    enum: assetStandardType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "number",
    label: "地块数"
    // width: 115,
    // search: { el: "input", tooltip: "我是搜索提示" }
  },
  {
    prop: "sum_weight",
    label: "重量(斤)"
    // fieldNames: { label: "label", value: "value" },
    // search: { el: "select" }
  },
  {
    prop: "sum_value",
    label: "价值（元）",
    width: 190
    // fieldNames: { label: "label", value: "value" }
    // search: { el: "select" }
  },
  {
    prop: "f_date",
    label: "创建日期",
    // width: 110,
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  }
]);

//手动更新草地资产
const updateData = async () => {
  ElMessageBox.confirm("此操作会对系统内所有草地数据进行计算，需要一定处理时间，确定要现在更新吗", "温馨提示", {
    type: "warning"
  }).then(async () => {
    await updateGrassAsset();
    // window.location.reload();
  });
};

// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportGrassInfo, "草地资产导出结果", proTable.value?.searchParam)
  );
};
//导出所选数据
const downloadSelectFile = async selectedListIds => {
  // 获取用户在表格中所选数据
  const selectedGrassData = selectedListIds;

  if (!selectedGrassData || selectedGrassData.length === 0) {
    ElMessage.warning("请先选择要导出的数据！");
    return;
  }

  ElMessageBox.confirm(`确认导出所选的${selectedGrassData.length}条数据?`, "温馨提示", { type: "warning" }).then(() => {
    // 调用useDownload函数进行导出，并传入所选数据
    useDownload(() => exportGrassInfo(selectedGrassData), `草地资产导出结果`, null);
  });
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    // api: title === "新增" ? addManu : title === "编辑" ? editManu : undefined,
    getTableList: proTable.value?.getTableList
  };
  console.log(params);
  drawerRef.value?.acceptParams(params);
};
</script>
