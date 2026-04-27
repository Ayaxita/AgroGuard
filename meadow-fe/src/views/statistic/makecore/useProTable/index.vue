<template>
  <div class="table-box">
    <ProTable
      ref="proTable"
      :columns="columns"
      :request-api="getTableList"
      :data-callback="dataCallback"
      @drag-sort="sortTable"
      :search-col="4"
      :pagination="false"
    >
      <!-- :pagination="false"不显示分页了，直接把12条数据全部显示在一页了，要不改分页还得改总的 -->
      <!-- 表格 header 按钮 -->
      <template #tableHeader></template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
      <!-- 表格操作 -->
      <template #operation="scope">
        <!-- <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button> -->
        <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)">编辑</el-button>
      </template>
    </ProTable>
    <GrassDrawer ref="drawerRef" />
    <!-- <ImportExcel ref="dialogRef" /> -->
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
import { getManuList, editManu } from "../api/manu";

import {
  BooleanType,
  colorType,
  gene_aType,
  purposeType,
  rankType,
  sexType,
  stateType,
  varietyType,
  Lamb_statType,
  DoImmType,
  d_plantcareResult2Type,
  BrucellaType
} from "@/assets/json/typeListJson";
import { useDownload } from "@/hooks/useDownload";

const router = useRouter();

// ProTable 实例
const proTable = ref<ProTableInstance>();

// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return data.list; //草了，分页去了害的把这个改了，真傻比
  // return {
  //   list: data.list
  //   // total: data.total
  // };
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
  { prop: "operation", label: "操作", fixed: "left", width: 80 },
  {
    prop: "variety",
    label: "草地类型",
    width: 90,
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
    prop: "gene_a",
    label: "多批基因",
    enum: gene_aType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "fetus_num",
    label: "同批次数(批)"
  },
  {
    prop: "birth_weight_1",
    label: "初始生物量（一批）/(kg)",
    width: 100
  },
  {
    prop: "birth_weight_2",
    label: "初始生物量（两批）/(kg)",
    width: 100
  },
  {
    prop: "birth_weight_3",
    label: "初始生物量（多批）/(kg)",
    width: 100
  },
  {
    prop: "weaning_weight_1",
    label: "阶段生物量（一批）/(kg)",
    width: 100
  },
  {
    prop: "weaning_weight_2",
    label: "阶段生物量（两批）/(kg)",
    width: 100
  },
  {
    prop: "weaning_weight_3",
    label: "阶段生物量（多批）/(kg)",
    width: 100
  },
  {
    prop: "weight_six",
    label: "生物量（生长月6）/(kg)",
    width: 100
  },
  {
    prop: "weight_twelve",
    label: "生物量（生长月12）/(kg)",
    width: 110
  },
  {
    prop: "weight_twenty_four",
    label: "生物量（生长月24）/(kg)",
    width: 110
  },
  {
    prop: "height_2",
    label: "株高（生长月2）/(cm)",
    width: 100
  },
  {
    prop: "height_6",
    label: "株高（生长月6）/(cm)",
    width: 100
  },
  {
    prop: "height_12",
    label: "株高（生长月12）/(cm)",
    width: 110
  },
  {
    prop: "height_24",
    label: "株高（生长月24）/(cm)",
    width: 110
  },
  {
    prop: "length_2",
    label: "茎长（生长月2）/(cm)",
    width: 100
  },
  {
    prop: "length_6",
    label: "茎长（生长月6）/(cm)",
    width: 100
  },
  {
    prop: "length_12",
    label: "茎长（生长月12）/(cm)",
    width: 110
  },
  {
    prop: "length_24",
    label: "茎长（生长月24）/(cm)",
    width: 110
  },
  {
    prop: "bust_2",
    label: "冠幅（生长月2）/(cm)",
    width: 100
  },
  {
    prop: "bust_6",
    label: "冠幅（生长月6）/(cm)",
    width: 100
  },
  {
    prop: "bust_12",
    label: "冠幅（生长月12）/(cm)",
    width: 110
  },
  {
    prop: "bust_24",
    label: "冠幅（生长月24）/(cm)",
    width: 110
  },
  {
    prop: "back_fat_2",
    label: "茎径（生长月2）/(cm)",
    width: 110
  },
  {
    prop: "back_fat_6",
    label: "茎径（生长月6）/(cm)",
    width: 110
  },
  {
    prop: "back_fat_12",
    label: "茎径（生长月12）/(cm)",
    width: 120
  },
  {
    prop: "back_fat_24",
    label: "茎径（生长月24）/(cm)",
    width: 120
  },
  {
    prop: "eye_muscle_2",
    label: "叶面积（生长月2）/(cm²)",
    width: 120
  },
  {
    prop: "eye_muscle_6",
    label: "叶面积（生长月6）/(cm²)",
    width: 120
  },
  {
    prop: "eye_muscle_12",
    label: "叶面积（生长月12）/(cm²)",
    width: 120
  },
  {
    prop: "eye_muscle_24",
    label: "叶面积（生长月24）/(cm²)",
    width: 120
  },
  {
    prop: "daily_weight_gain",
    label: "日均增量(前6个月)/(g)",
    width: 130
  },
  {
    prop: "born_per_year_1",
    label: "平均年采收次数（一档）/(次)",
    width: 130
  },
  {
    prop: "born_per_year_2",
    label: "平均年采收次数（二档）/(次)",
    width: 130
  },
  {
    prop: "m_birth_num_1",
    label: "生长中期-采收次数(一档)/(次)",
    width: 130
  },
  {
    prop: "m_birth_num_2",
    label: "生长中期-采收次数(二档)/(次)",
    width: 130
  },
  {
    prop: "f_birth_num",
    label: "生长初期-采收次数/(次)",
    width: 110
  },
  {
    prop: "n_birth_num",
    label: "休眠期-采收次数/(次)",
    width: 110
  },
  {
    prop: "survival_rate",
    label: "存活率/(%)",
    width: 110
  },
  {
    prop: "lambs_per_year",
    label: "年收割次数/(次)",
    width: 110
  },
  {
    prop: "m_lambs_year",
    label: "生长中期-年收割次数/(次)",
    width: 130
  },
  {
    prop: "f_lambs_year",
    label: "生长初期-产出批次数/(个)",
    width: 130
  },
  {
    prop: "n_lambs_year",
    label: "非生长期-产出批次数/(个)",
    width: 130
  },
  {
    prop: "small_rum",
    label: "植保药剂",
    enum: DoImmType,
    search: { el: "select" },
    width: 110
  },
  {
    prop: "fmd",
    label: "真菌病防护剂",
    enum: DoImmType,
    search: { el: "select" },
    width: 110
  },
  {
    prop: "grass_pox",
    label: "锈病防护剂",
    enum: DoImmType,
    search: { el: "select" },
    width: 110
  },
  {
    prop: "tnq",
    label: "综合防护剂",
    search: { el: "select" },
    enum: DoImmType,
    width: 120
  },
  {
    prop: "brucella",
    label: "根腐病检测",
    enum: BrucellaType,
    search: { el: "select" },
    width: 110
  },

  {
    prop: "note",
    label: "备注信息",
    search: {
      el: "input",
      props: {
        type: "textarea"
      }
    }
  }

  // {
  //   prop: "score",
  //   label: "综合长势评分",
  //   search: {
  //     el: "input",
  //     props: {
  //       type: "number"
  //     }
  //   }
  // }
]);

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    // api: title === "入棚" ? addManu : title === "编辑" ? editManu : undefined,
    api: title === "编辑" ? editManu : undefined,

    getTableList: proTable.value?.getTableList
  };
  console.log(params);
  drawerRef.value?.acceptParams(params);
};
</script>
