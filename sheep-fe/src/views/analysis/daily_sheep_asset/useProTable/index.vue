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
      <template #tableHeader>
        <el-button type="primary" :icon="Refresh" @click="updateData">更新数据</el-button>
        <!-- <el-button type="primary" :icon="Refresh" @click="updateDataAll">统计数据</el-button> -->
        <!-- <el-button type="danger" :icon="Delete" @click="deleteData">删除</el-button> -->
        <!-- <el-button type="primary" :icon="Download" plain @click="downloadFile">导出所选数据</el-button> -->
        <el-button type="primary" :icon="Download" plain @click="downloadFile">导出数据</el-button>
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
    <SheepDrawer ref="drawerRef" />
    <ImportExcel ref="dialogRef" />
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { User } from "@/api/interface";
import { ElMessage, ElMessageBox } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import SheepDrawer from "../components/SheepDrawer.vue";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { CirclePlus, Delete, Download, EditPen, View, Refresh } from "@element-plus/icons-vue";
import { getManuList, editManu, updateDailyIncome, updateSheepAsset, exportSheepInfo } from "../api/manu";
import { InventoryTypeType, varietyType } from "@/assets/json/typeListJson";
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
  // { type: "selection", fixed: "left", width: 70 },
  // { prop: "operation", label: "操作", fixed: "left", width: 80 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "huyang",
    label: "禾本科草",
    _children: [
      {
        prop: "zhongyang",
        label: "种苗",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "hu_0_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "hu_0_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      },
      {
        prop: "yufei",
        label: "生长期草地",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "hu_1_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "hu_1_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      },
      {
        prop: "buru",
        label: "幼苗批次(1月)",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "hu_2_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "hu_2_0",
                label: "价值(元)"
              }
            ]
          }
        ]
      },
      {
        prop: "buru2",
        label: "幼苗批次(2月)",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "hu_3_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "hu_3_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    prop: "xiaowei",
    label: "豆科草",
    _children: [
      {
        prop: "zhongyang",
        label: "种苗",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "xw_0_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "xw_0_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      },
      {
        prop: "yufei",
        label: "生长期草地",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "xw_1_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "xw_1_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      },
      {
        prop: "buru1",
        label: "幼苗批次(1月)",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "xw_2_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "xw_2_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      },
      {
        prop: "buru2",
        label: "幼苗批次(2月)",
        _children: [
          {
            prop: "gong",
            label: "A组",
            _children: [
              {
                prop: "xw_3_0",
                label: "价值(元)"
              }
            ]
          },
          {
            prop: "mu",
            label: "B组",
            _children: [
              {
                prop: "xw_3_1",
                label: "价值(元)"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    prop: "f_date",
    label: "记录日期",
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

// 如果表格需要初始化请求参数，直接定义传给 ProTable(之后每次请求都会自动带上该参数，此参数更改之后也会一直带上，改变此参数会自动刷新表格数据)
const initParam = reactive({ departmentId: "1" });

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};
//todo
//删除
const deleteData = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

//手动更新日收入统计
const updateData = async () => {
  ElMessageBox.confirm("如果数据量过大可能会等待一些时间，确定要现在更新吗", "温馨提示", { type: "warning" }).then(async () => {
    await updateSheepAsset();
    window.location.reload();
  });
};

// const updateDataAll = async () => {
//   ElMessageBox.confirm("如果数据量过大可能会等待一些时间，确定要现在更新吗", "温馨提示", { type: "warning" }).then(async () => {
//     await updateALL();
//     // window.location.reload();
//   });
// };

// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportSheepInfo, "草地库存资产导出结果", proTable.value?.searchParam)
  );
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof SheepDrawer> | null>(null);
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
