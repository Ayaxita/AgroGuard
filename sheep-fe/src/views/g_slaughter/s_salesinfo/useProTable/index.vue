<template>
  <div class="table-box">
    <ProTable ref="proTable" :columns="columns" :request-api="getTableList" :data-callback="dataCallback" :search-col="4">
      <!-- 表格 header 按钮 -->
      <!-- 草地记录销售从基本信息表读取，操作 -->
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
import { EditPen, View } from "@element-plus/icons-vue";
import { getManuList, editManu, addManu } from "../api/manu";

import { useDownload } from "@/hooks/useDownload";
import { BooleanType, G_slaughterTypeType, SellingType } from "@/assets/json/typeListJson";

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
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "sales_date",
    label: "销售日期",
    width: 150,
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
    prop: "sales_order",
    label: "销售单号",
    width: 115,
    search: {
      el: "input"
    }
  },
  {
    prop: "type",
    label: "类型",
    enum: G_slaughterTypeType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "quarantine_coding",
    label: "检测编码",
    width: 150,
    search: {
      el: "input"
    }
  },
  {
    prop: "ele_num",
    label: "草地编号",
    width: 150,
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
    prop: "medical_leave",
    label: "是否执行安全间隔期",
    enum: BooleanType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "billing_unit",
    label: "计费单位",
    search: {
      el: "input"
    }
  },
  {
    prop: "unit_price",
    label: "单价",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "total_price",
    label: "总价",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "transportation",
    label: "运输方式",
    search: {
      el: "input"
    }
  },
  {
    prop: "sales_site",
    label: "销售地点",
    search: {
      el: "input"
    }
  },
  {
    prop: "name",
    label: "销往单位名称",
    search: {
      el: "input"
    }
  },
  {
    prop: "buyer",
    label: "买方联系人",
    search: {
      el: "input"
    }
  },
  {
    prop: "buyer_phone",
    label: "买方电话",
    search: {
      el: "input"
    }
  },
  {
    prop: "selling_type",
    label: "销往对象类型",
    enum: SellingType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "notes",
    label: "备注信息",
    search: {
      el: "input",
      props: {
        type: "textarea"
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
  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);

// // 表格拖拽排序
// const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
//   console.log(newIndex, oldIndex);
//   console.log(proTable.value?.tableData);
//   ElMessage.success("修改列表排序成功");
// };
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
  //   useDownload(exportSheepInfo, "羊只导出结果", proTable.value?.searchParam)
  // );
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
</script>
