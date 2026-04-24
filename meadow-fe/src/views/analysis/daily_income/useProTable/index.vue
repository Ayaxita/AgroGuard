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
        <el-button type="primary" :icon="Refresh" @click="updateData">更新当日数据</el-button>
        <el-button type="primary" :icon="Refresh" @click="updateSelectData(scope.selectedList)">更新所选日期数据</el-button>
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
import { getManuList, editManu, updateDailyIncome, exportGrassInfo, updateSelectDailyIncome } from "../api/manu";
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
  { type: "selection", fixed: "left", width: 70 },
  // { prop: "operation", label: "操作", fixed: "left", width: 80 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "sell",
    label: "草地记录销售",
    _children: [
      {
        prop: "sell_0",
        label: "种苗销售",
        _children: [
          {
            prop: "number_0",
            label: "条数"
          },
          {
            prop: "value_0",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "sell_1",
        label: "生长期销售",
        _children: [
          {
            prop: "number_1",
            label: "条数"
          },
          {
            prop: "value_1",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "sell_2",
        label: "幼苗批次销售",
        _children: [
          {
            prop: "number_2",
            label: "条数"
          },
          {
            prop: "value_2",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "sell_3",
        label: "淘汰地块销售",
        _children: [
          {
            prop: "number_3",
            label: "条数"
          },
          {
            prop: "value_3",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "sell_9",
        label: "其他",
        _children: [
          {
            prop: "number_9",
            label: "条数"
          },
          {
            prop: "value_9",
            label: "销售额(元)"
          }
        ]
      }
    ]
  },
  {
    prop: "spin_off_sell",
    label: "草地副产品销售",
    _children: [
      {
        prop: "dung_sell",
        label: "草地残渣",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "dung_value",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "wool_sell",
        label: "采收产物",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "wool_value",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "skin_sell",
        label: "地表覆盖物",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "skin_value",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "manure_sell",
        label: "有机肥",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "manure_value",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "feed_sell",
        label: "草地投入物",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "feed_value",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "producted_sell",
        label: "草地副产物",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "producted_value",
            label: "销售额(元)"
          }
        ]
      },
      {
        prop: "other_sell",
        label: "其他",
        _children: [
          // {
          //   prop: "maker_name",
          //   label: "只数",
          //   search: { el: "input" }
          // },
          {
            prop: "other_value",
            label: "销售额(元)"
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
const updateSelectData = async parmas => {
  if (!parmas || parmas.length === 0) {
    ElMessage.warning("请先选择要更新的数据！");
    return;
  }
  if (parmas.length > 1) {
    ElMessage.warning("只能选择一条更新的数据！");
    return;
  }
  ElMessageBox.confirm("确定要现在更新吗", "温馨提示", { type: "warning" }).then(() => {
    console.log(parmas);

    updateSelectDailyIncome(parmas);
    window.location.reload();
  });
};

//手动更新日收入统计
const updateData = async () => {
  ElMessageBox.confirm("如果数据量过大可能会等待一些时间，确定要现在更新吗", "温馨提示", { type: "warning" }).then(() => {
    updateDailyIncome();
    window.location.reload();
  });
};

// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportGrassInfo, "日收入报表导出结果", proTable.value?.searchParam)
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
