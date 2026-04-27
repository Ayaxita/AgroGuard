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
        <el-button type="danger" :icon="Delete" @click="deleteHouseinfo(scope.selectedListIds)">删除</el-button>
        <el-button type="primary" :icon="Refresh" plain @click="updateHouse">清点数量</el-button>
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
import { CirclePlus, Delete, EditPen, Refresh, View } from "@element-plus/icons-vue";
import { getManuList, editManu, addManu, delManu, updateHouseNumber } from "../api/manu";
import { fieldFuntionType, fieldH_typeType, varietyType } from "@/assets/json/typeListJson";

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
  { prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "id",
    label: "编号",
    width: 60,
    search: {
      el: "input"
    }
  },
  {
    prop: "name",
    label: "监测站点名称",
    width: 130,
    search: {
      el: "input"
    }
  },
  {
    prop: "function",
    label: "功能",
    width: 120,
    enum: fieldFuntionType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "area",
    label: "面积(平方米)",
    search: {
      el: "input",
      props: { type: "number" }
    }
  },
  {
    prop: "h_type",
    label: "区域类型",
    enum: fieldH_typeType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "h_lwh",
    label: "区域尺寸",
    search: {
      el: "input"
    }
  },
  {
    prop: "sports_lwh",
    label: "生长区尺寸",
    width: 110,
    search: {
      el: "input"
    }
  },
  {
    prop: "grass_type",
    label: "草地类型",
    width: 110,
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "area_pro",
    label: "草地覆盖率",
    search: {
      el: "input"
    }
  },
  {
    prop: "grass_quantity",
    label: "地块数量",
    search: {
      el: "input",
      props: { type: "number" }
    }
  },
  // {
  //   prop: "difinfect_time",
  //   label: "最后防疫时间",
  //   search: {
  //     el: "date-picker",
  //     props: {
  //       type: "daterange",
  //       format: "YYYY-MM-DD",
  //       "value-format": "YYYY-MM-DD"
  //     }
  //   }
  // },
  {
    prop: "build_time",
    label: "建设时间",
    width: 115,
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
    prop: "staff",
    label: "管理人员",
    search: {
      el: "input"
    }
  }
  // {
  //   prop: "f_staff",
  //   label: "创建人员",
  //   search: {
  //     el: "input"
  //   }
  // }
]);
// 清点数量
const updateHouse = async () => {
  ElMessageBox.confirm("此操作会根据已有的草地数据，对监测站点的地块数量进行更新，并计算覆盖率，确认更新吗？", "温馨提示", {
    type: "warning"
  }).then(() =>
    updateHouseNumber().then(() => {
      ElMessage.success("更新成功！");
      proTable.value?.getTableList();
    })
  );
};
// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

//删除
const deleteHouseinfo = ids => {
  if (ids.length !== 0) {
    ElMessageBox.confirm(`确认删除监测站点?<br/>已选${ids.length}条记录`, "温馨提示", {
      type: "warning",
      dangerouslyUseHTMLString: true
    }).then(() => {
      delManu(ids).then(res => {
        if (res.code === 200) {
          ElMessage.success("删除成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要删除的监测站点！");
  }
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
