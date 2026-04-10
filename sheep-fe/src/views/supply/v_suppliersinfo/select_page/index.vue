<template>
  <div class="table-box">
    <ProTable ref="proTable" :columns="columns" :request-api="getTableList" :data-callback="dataCallback" :search-col="2">
      <!-- 表格 header 按钮 -->
      <template #tableHeader="scope">
        <el-button type="primary" :icon="Select" @click="selectMaker(scope.selectedList)">选择</el-button>
      </template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
    </ProTable>
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive } from "vue";
import { User } from "@/api/interface";
import ProTable from "@/components/ProTable/index.vue";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { Select } from "@element-plus/icons-vue";
import { getSupplyList } from "../api/manu";
import { ElMessage } from "element-plus";

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
  return getSupplyList(params);
};

// 选择
const selectMaker = ids => {
  if (ids.length === 1) {
    let win = window.opener;
    win.postMessage({ ...ids[0] }, window.location.origin);
    window.close();
  } else if (ids.length !== 0) {
    ElMessage.warning("只能选择一个厂商");
  } else {
    ElMessage.warning("请选择厂商");
  }
};

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  {
    prop: "supplier_name",
    label: "厂商名称",
    search: { el: "input" }
  },
  {
    prop: "sale_type",
    label: "防护剂类型",
    search: {
      el: "input",
      props: {
        type: "textarea"
      }
    }
  },
  {
    prop: "sup_linkman",
    label: "联系人",
    search: { el: "input" }
  },
  {
    prop: "sup_contact",
    label: "联系人电话",
    search: { el: "input" }
  },
  {
    prop: "contact",
    label: "厂商电话",
    search: { el: "input" }
  },
  {
    prop: "mail",
    label: "邮箱",
    search: { el: "input" }
  },
  {
    prop: "address",
    label: "地址",
    search: { el: "input" }
  },
  {
    prop: "f_date",
    label: "创建时间",
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
    search: { el: "input" }
  }
]);
</script>
