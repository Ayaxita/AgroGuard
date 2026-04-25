<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :size="drawerWidth" :title="`${drawerProps.title}`">
    <div class="drawer-container">
      <!-- 左侧：搜索框和表格 -->
      <div class="left-section">
        <!-- ProTable -->
        <ProTable
          v-if="showSearch"
          ref="proTable"
          :columns="columns"
          :request-api="getTableList"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectColony(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>

        <ProTable
          v-if="showSearchHurdle"
          ref="proTable"
          :columns="columns"
          :request-api="getHurdleListWithSelectedHouse"
          :init-param="initParam"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-select v-model="selectedHouse" filterable placeholder="请先选择所属区域" style="width: 240px">
              <el-option v-for="item in houses" :key="item.value" :value="item.value" :label="item.label" />
            </el-select>
            <el-button type="primary" :icon="CirclePlus" @click="selectHurdle(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>
      </div>
      <!-- 右侧：表单内容 -->
      <div
        class="right-section"
        :style="{
          right: drawerVisible ? `${drawerWidth}px` : '0px'
        }"
      >
        <el-form
          ref="ruleFormRef"
          label-width="160px"
          label-suffix=" :"
          :rules="rules"
          :disabled="drawerProps.isView"
          :model="drawerProps.row"
          :hide-required-asterisk="drawerProps.isView"
        >
          <!-- Integer fields -->
          <el-form-item label="草地类型" prop="variety">
            <el-select v-model="drawerProps.row.variety" clearable>
              <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="作物类型" prop="sex">
            <el-select v-model="drawerProps.row.sex" clearable>
              <el-option v-for="item in sexType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="草地记录类别" prop="purpose">
            <el-select v-model="drawerProps.row.purpose" clearable>
              <el-option v-for="item in assetStandardType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <!-- Float fields -->
          <el-form-item label="单价" prop="unit_price">
            <el-input v-model.number="drawerProps.row.unit_price" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="特级" prop="rank_0">
            <el-input v-model.number="drawerProps.row.rank_0" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="一级" prop="rank_1">
            <el-input v-model.number="drawerProps.row.rank_1" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="二级" prop="rank_2">
            <el-input v-model.number="drawerProps.row.rank_2" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="三级" prop="rank_3">
            <el-input v-model.number="drawerProps.row.rank_3" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="未评级" prop="rank_9">
            <el-input v-model.number="drawerProps.row.rank_9" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="操作人" prop="f_staff">
            <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
          </el-form-item>
          <el-form-item label="创建时间" prop="f_date">
            <el-date-picker
              v-model="drawerProps.row.f_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="创建时间会自动填入"
              disabled
              clearable
            />
          </el-form-item>
          <el-form-item label="备注信息" prop="note">
            <el-input v-model="drawerProps.row.note" type="textarea" clearable></el-input>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <template #footer>
      <div class="drawer-footer">
        <el-button @click="drawerVisible = false">取消</el-button>
        <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="SheepDrawer">
import { ref, reactive, computed, onBeforeMount } from "vue";
import { User } from "@/api/interface";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import ProTable from "@/components/ProTable/index.vue";
import { ElMessage, FormInstance, ElMessageBox } from "element-plus";
import { CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import {
  colonyFuntionType,
  colonyH_typeType,
  colorType,
  gene_aType,
  Lamb_statType,
  purposeType,
  rankType,
  sexType,
  stateType,
  d_healthResult2Type,
  DoImmType,
  varietyType,
  assetStandardType
} from "@/assets/json/typeListJson";
import UploadImg from "@/components/Upload/Img.vue";
import { getManuList as getHurdle } from "@/views/colony/hurdleinfo/api/manu";
import { getManuList } from "@/views/colony/houseinfo/api/manu";

const rules = reactive({
  // breeding_id: [
  //   {
  //     required: true,
  //     message: "请填写培育信息id"
  //   }
  // ],
  // tobasic: [
  //   {
  //     required: true,
  //     message: "请设置是否入库"
  //   }
  // ],
  // pre_num: [
  //   {
  //     required: true,
  //     message: "请填写防疫耳号"
  //   }
  // ]
});
// 控制搜索框和表格的显示
const showSearch = ref(false);
// 控制搜索框和表格的显示
const showSearchHurdle = ref(false);
const houses = ref<any>([]);
const selectedHouse = ref("");
const selectedHurdle = ref("");
// 如果表格需要初始化请求参数，直接定义传给 ProTable (之后每次请求都会自动带上该参数，此参数更改之后也会一直带上，改变此参数会自动刷新表格数据)
const initParam = reactive({ house_id: selectedHouse });

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  // { prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "id",
    label: "编号",
    search: {
      el: "input"
    }
  },
  {
    prop: "name",
    label: "区段名称",
    search: {
      el: "input"
    }
  },
  {
    prop: "function",
    label: "功能",
    enum: colonyFuntionType,
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
    label: "监测区类型",
    enum: colonyH_typeType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "h_lwh",
    label: "监测区域长宽高",
    search: {
      el: "input"
    }
  },
  {
    prop: "sports_lwh",
    label: "运动场长宽高",
    search: {
      el: "input"
    }
  },
  {
    prop: "sheep_type",
    label: "草地记录类型",
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "area_pro",
    label: "草地记录面积比例",
    search: {
      el: "input"
    }
  },
  {
    prop: "sheep_quantity",
    label: "草地记录数量",
    search: {
      el: "input",
      props: { type: "number" }
    }
  },
  {
    prop: "build_time",
    label: "建设时间",
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
    prop: "difinfect_time",
    label: "最后消毒时间",
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

// 切换显示搜索框和表格,并搜索信息
const toggleSearchTable = () => {
  console.log(showSearch.value);

  showSearch.value = !showSearch.value;
};
// 切换显示搜索框和表格,并搜索信息
const toggleSearchHurdkeTable = () => {
  console.log("showSearchHurdle", showSearchHurdle.value);

  showSearchHurdle.value = !showSearchHurdle.value;
  console.log(showSearchHurdle.value);
  console.log("showSearch", showSearch.value);

  console.log(selectedHouse.value);
};

// 选择棚舍后，更新圈舍名称和house_id，并初始化栏舍选择表格
const selectColony = async (selectedList: any) => {
  if (selectedList.length === 0) {
    ElMessage.warning("请选择要添加的监测区域");
    return;
  }

  // 获取选中的棚舍
  const selectedHouseItem = selectedList[0];

  // 更新圈舍名称和 house_id
  drawerProps.value.row.house_name = selectedHouseItem.name; // 设置圈舍名称
  drawerProps.value.row.house_id = selectedHouseItem.id;
  selectedHouse.value = selectedHouseItem.id; // 更新 house_id

  // 关闭棚舍选择表格
  showSearch.value = false;
};

const getHurdleListWithSelectedHouse = async params => {
  if (!selectedHouse.value) {
    ElMessage.warning("请先选择监测区域");
    return { list: [], total: 0 }; // 返回空数据
  }

  try {
    // 请求数据并处理返回结果
    const data = await getTableList1({ ...params, house_id: selectedHouse.value });
    console.log("获取到的数据", data);
    // 假设返回的结果是 { list: [], total: 0 }
    return data;
  } catch (error) {
    console.error("获取数据失败", error);
    ElMessage.error("数据请求失败");
    return { list: [], total: 0 }; // 出现错误时返回空数据
  }
};

// 选择栏舍后，更新圈栏名称和house_id，
const selectHurdle = async (selectedList: any) => {
  if (selectedList.length === 0) {
    ElMessage.warning("请选择要添加的区段");
    return;
  }

  // 获取选中的棚舍
  const selectedHurdleItem = selectedList[0];

  // 更新圈舍名称和 house_id
  drawerProps.value.row.hurdle_name = selectedHurdleItem.name; // 设置圈舍名称
  drawerProps.value.row.hurdle_id = selectedHurdleItem.id;
  selectedHurdle.value = selectedHurdleItem.id; // 更新 house_id

  // 关闭棚舍选择表格
  showSearchHurdle.value = false;
};

// ProTable 实例引用
const proTable = ref<ProTableInstance>();

// 动态调整宽度
const drawerWidth = computed(() => {
  // return showSearch.value ? `${window.innerWidth}px` : "450px";
  // 根据 showSearch 或 showSearchHurdle 的值调整宽度
  if (showSearch.value || showSearchHurdle.value) {
    return `${window.innerWidth}px`; // 当 showSearch 或 showSearchHurdle 为 true 时，设置宽度为浏览器窗口宽度
  } else {
    return "450px"; // 否则设置为固定宽度
  }
});
// 导出列表
// const selectColony = async selectedList => {
//   console.log(selectedList);
//   if (selectedList.length == 0) {
//     ElMessage.warning("请选择要添加的栏舍");
//     return;
//   } else if (selectedList.length > 1) {
//     // ElMessageBox.confirm("只能选择1株?", "温馨提示", { type: "warning" });
//     ElMessage.warning("只能选择一个记录");
//     return;
//   }
//   // 获取选中记录的 ele_num 值
//   const selectedColony = selectedList[0].name;

//   // 确认提示
//   try {
//     await ElMessageBox.confirm(`确认选择电子耳号为 ${selectedColony} 的母系草地?`, "温馨提示", {
//       type: "warning"
//     });

//     // 将选中的 ele_num 值写入表单数据
//     drawerProps.value.row.house = selectedColony.name;

//     ElMessage.success("草地编号已成功添加");
//   } catch (error) {
//     console.log("操作取消");
//   }
// };

//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getManu", getManuList(newParams));
  return getManuList(newParams);
};

const getTableList1 = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getHuidle", getHurdle(newParams));
  console.log("showSearchHurdle", showSearchHurdle);

  return getHurdle(newParams);
};

// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};

interface DrawerProps {
  title: string;
  isView: boolean;
  // row: Partial<User.ResUserList>;
  row: any;
  api?: (params: any) => Promise<any>;
  getTableList?: () => void;
}

const drawerVisible = ref(false);
const drawerProps = ref<DrawerProps>({
  isView: false,
  title: "",
  row: {}
});

// 接收父组件传过来的参数
const acceptParams = (params: DrawerProps) => {
  drawerProps.value = params;
  drawerVisible.value = true;
  showSearch.value = false;
  showSearchHurdle.value = false;
};

// 提交数据（新增/编辑）
const ruleFormRef = ref<FormInstance>();
const handleSubmit = () => {
  ruleFormRef.value!.validate(async valid => {
    if (!valid) return;
    try {
      console.log("drawerProps.value.row", drawerProps.value.row);
      await drawerProps.value.api!(drawerProps.value.row);
      ElMessage.success({ message: `${drawerProps.value.title}成功！` });
      drawerProps.value.getTableList!();
      drawerVisible.value = false;
    } catch (error) {
      console.log(error);
    }
  });
};

defineExpose({
  acceptParams
});
</script>
<style scoped>
.drawer-container {
  position: relative;
  display: flex;
  height: 100%;
}
.left-section {
  flex: 1;
  max-width: calc(100% - 450px); /* 确保左侧不会挤压右侧 */
  overflow: auto;
  background-color: #f5f5f5; /* 示例背景色，可按需调整 */
}
.right-section {
  position: fixed;
  top: 55px;
  right: 50px;
  width: 400px;
  height: 85vh;
  padding-top: 20px;
  overflow-y: auto;
  background-color: #ffffff;
  box-shadow: -2px 0 5px rgb(0 0 0 / 10%); /* 添加阴影效果 */
}
.drawer-footer {
  position: sticky;
  bottom: 0; /* 固定在底部 */
  z-index: 100; /* 确保在右侧div之上 */
  width: 100%;
  background-color: #ffffff;
}
.ml-1 {
  margin-bottom: 10px;
}
.ml-2 {
  margin-bottom: 10px;
}
.el-message {
  z-index: 9999 !important; /* 调整为更高的值 */
}
</style>
