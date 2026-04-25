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
        <el-button type="danger" :icon="Delete" @click="deleteData">删除</el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadFile">导出所选数据</el-button>
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
import { Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import { getManuList, editManu, addManu } from "../api/manu";
import { colorType, gene_aType, purposeType, rankType, sexType, stateType, varietyType } from "@/assets/json/typeListJson";
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
  { type: "sort", label: "Sort", width: 80 },
  { type: "expand", label: "Expand", width: 85 },
  {
    prop: "basic_id",
    label: "草地基本信息ID",
    search: {
      el: "input"
    }
  },
  {
    prop: "age",
    label: "生长年数",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "house_id",
    label: "圈舍号",
    search: {
      el: "input",
      props: {
        type: "number"
      }
    }
  },
  {
    prop: "in_weight",
    label: "入栏体重",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "in_1_5",
    label: "入栏1.5月体重",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "in_3",
    label: "入栏3月体重",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "in_4_5",
    label: "入栏4.5月体重",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "out_weight",
    label: "出栏体重",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "put_volume",
    label: "投放量（每1.5个月）",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "intake",
    label: "草地投入量（每1.5个月）",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "menu",
    label: "草地投入物种类",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "cost",
    label: "成本",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "FCR",
    label: "草地投入转化效率",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "ADG",
    label: "日均增量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "f_staff",
    label: "创建人员",
    search: {
      el: "input"
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
const deleteData = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};
// 导出列表
const downloadFile = async () => {
  // ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
  //   useDownload(exportGrassInfo, "草地导出结果", proTable.value?.searchParam)
  // );
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
