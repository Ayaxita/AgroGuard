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
            <el-button type="primary" :icon="CirclePlus" @click="selectEwe(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>

        <ProTable
          v-if="showSearchRam"
          ref="proTable"
          :columns="columns"
          :request-api="getTableList1"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectRam(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>
      </div>
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
          <!-- 关联信息编号 -->
          <el-form-item v-if="false" label="关联编号1" prop="ewe_ele_num">
            <el-input v-model="drawerProps.row.ewe_ele_num" type="text" clearable :disabled="isEditMode"></el-input>
            <el-button @click="toggleSearchTable" size="small" type="primary" class="ml-1" :disabled="isEditMode">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              添加关联信息
            </el-button>
          </el-form-item>
          <!-- 关联类型 -->
          <el-form-item v-if="false" label="关联类型" prop="ewe_variety">
            <el-select v-model="drawerProps.row.ewe_variety" clearable :disabled="isEditMode">
              <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <!-- 关联信息编号 -->
          <el-form-item v-if="false" label="关联编号2" prop="ram_ele_num">
            <el-input v-model="drawerProps.row.ram_ele_num" type="text" clearable :disabled="isEditMode"></el-input>
            <el-button @click="toggleSearchRamTable" size="small" type="primary" class="ml-2" :disabled="isEditMode">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              添加关联信息
            </el-button>
          </el-form-item>
          <!-- 关联类型2 -->
          <el-form-item v-if="false" label="关联类型2" prop="ram_variety">
            <el-select v-model="drawerProps.row.ram_variety" clearable :disabled="isEditMode">
              <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="false">
            <el-button @click="judgeInbreed" size="small" type="primary" class="ml-3"> 近亲检测 </el-button>
          </el-form-item>
          <!-- 关联日期 -->
          <el-form-item v-if="false" label="关联日期" prop="breeding_date">
            <el-date-picker
              v-model="drawerProps.row.breeding_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
              @change="updatePreProductionDate"
              @clear="clearPreProductionDate"
            />
          </el-form-item>

          <!-- 预产日期 -->
          <el-form-item v-if="false" label="预产日期" prop="pre_production_date">
            <el-date-picker
              v-model="drawerProps.row.pre_production_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
              @clear="clearBreedingDate"
            />
          </el-form-item>

          <!-- 关联方式 -->
          <el-form-item v-if="false" label="关联方式" prop="breeding_way">
            <el-select v-model="drawerProps.row.breeding_way" clearable>
              <el-option v-for="item in Breeding_wayType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <!-- 关联状态 -->
          <el-form-item v-if="false" label="关联状态" prop="breeding_state">
            <el-select v-model="drawerProps.row.breeding_state" clearable>
              <el-option v-for="item in Breeding_stateType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <!-- 关联周期(天) -->
          <el-form-item v-if="false" label="关联周期(天)" prop="mat_period">
            <el-input type="number" v-model="drawerProps.row.mat_period" clearable></el-input>
          </el-form-item>

          <!-- 成功率(%) -->
          <el-form-item v-if="false" label="成功率(%)">
            <el-input v-model="drawerProps.row.single_ok" clearable></el-input>
          </el-form-item>

          <!-- 操作师 -->
          <el-form-item label="操作师" prop="staff">
            <el-input v-model="drawerProps.row.staff" clearable></el-input>
          </el-form-item>

          <!-- 创建时间 -->
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

          <!-- 创建人员 -->
          <el-form-item label="创建人员" prop="f_staff">
            <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
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

<script setup lang="ts" name="GrassDrawer">
import { ref, reactive, computed } from "vue";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import { CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import {
  Breeding_stateType,
  Breeding_wayType,
  colorType,
  d_healthCur_effectType,
  gene_aType,
  manuScaleType,
  manutypeType,
  purposeType,
  sexType,
  stateType,
  varietyType
} from "@/assets/json/typeListJson";
import { getEwe, getRam } from "../../postnatalinfo/api/manu";
import { ColumnProps } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { judgeInBreed } from "../api/manu";
import { getEweGrass } from "../../rutinfo/api/manu";
import { getRamGrass } from "../../semencollectinfo/api/manu";

const rules = reactive({
  staff: [{ required: true, message: "请输入操作师" }]
});
// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  // { prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "ele_num",
    label: "草地编号",
    width: 150,
    search: { el: "input" }
  },
  {
    prop: "pre_num",
    label: "地块编号",
    width: 115,
    search: { el: "input" }
  },
  {
    prop: "purpose",
    label: "用途",
    width: 115,
    enum: purposeType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "variety",
    label: "草地类型",
    width: 100,
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "color",
    label: "草地颜色",
    enum: colorType,
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
    prop: "birth",
    label: "播种日期",
    width: 110,
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
    prop: "wea_date",
    label: "阶段切换日期",
    width: 110,
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
    prop: "mon_age",
    label: "生长月数",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "manu_info_name",
    label: "原产地",
    width: 85,
    search: { el: "input" }
  },
  {
    prop: "state",
    label: "状态",
    enum: stateType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "house_name",
    label: "监测区域",
    width: 130,
    search: { el: "input" }
  },
  {
    prop: "hurdle_name",
    label: "监测地块",
    search: { el: "input" }
  },
  {
    prop: "gene_a",
    label: "多批基因",
    enum: gene_aType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  // {
  //   prop: "gene_b",
  //   label: "抗病基因",
  //   enum: gene_bType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: { el: "select" }
  // },
  // {
  //   prop: "gene_c",
  //   label: "待定基因",
  //   enum: gene_cType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: { el: "select" }
  // },
  {
    prop: "f_staff",
    label: "添加人",
    width: 115,
    search: { el: "input", tooltip: "我是搜索提示" }
  },
  {
    prop: "f_date",
    label: "添加时间",
    width: 110,
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
// 控制搜索框和表格的显示
const showSearch = ref(false);
const showSearchRam = ref(false);
// 切换显示搜索框和表格,并搜索信息
const toggleSearchTable = () => {
  console.log(showSearch.value);
  showSearchRam.value = false;
  showSearch.value = !showSearch.value;
};

// 切换显示搜索框和表格,并搜索信息
const toggleSearchRamTable = () => {
  showSearch.value = false;
  console.log("showSearchRam", showSearchRam.value);

  showSearchRam.value = !showSearchRam.value;
  console.log(showSearchRam.value);
  console.log("showSearch", showSearch.value);
};
//选择关联信息
const selectEwe = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的记录");
    return;
  } else if (selectedList.length > 1) {
    // ElMessageBox.confirm("只能选择1株?", "温馨提示", { type: "warning" });
    ElMessage.warning("只能选择一条记录");
    return;
  }
  // 获取选中记录的 ele_num 值
  const selectedItem = selectedList[0];

  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedItem.ele_num} 的记录?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    drawerProps.value.row.ewe_ele_num = selectedItem.ele_num;
    drawerProps.value.row.ewe_variety = selectedItem.variety;

    // 关闭选择表格
    showSearch.value = false;

    ElMessage.success("编号已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};
//选择关联信息
const selectRam = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的记录");
    return;
  } else if (selectedList.length > 1) {
    // ElMessageBox.confirm("只能选择1株?", "温馨提示", { type: "warning" });
    ElMessage.warning("只能选择一条记录");
    return;
  }
  // 获取选中记录的 ele_num 值
  const selectedItem = selectedList[0];

  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedItem.ele_num} 的记录?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    drawerProps.value.row.ram_ele_num = selectedItem.ele_num;
    drawerProps.value.row.ram_variety = selectedItem.variety;

    // 关闭选择表格
    showSearchRam.value = false;

    ElMessage.success("编号已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};

//近亲检测

interface InbreedResponse {
  code: number;
  msg: string;
  data: {
    boolean: boolean;
    list: any[]; // 根据需要，可以更具体地定义 list 的类型
  };
}

const judgeInbreed = async () => {
  // 获取编号
  const ram_ele_num = drawerProps.value.row.ram_ele_num;
  const ewe_ele_num = drawerProps.value.row.ewe_ele_num;

  // 将编号放入请求参数中
  const requestParams = {
    ram_ele_num,
    ewe_ele_num
  };

  console.log("请求的参数", requestParams);
  try {
    // 调用 judgeInBreed 方法，传递参数进行判断
    const response = await judgeInBreed(requestParams);

    // 类型断言，告诉 TypeScript response 是 InbreedResponse 类型
    const typedResponse = response as InbreedResponse;

    // 判断是否为成功返回
    if (typedResponse.code === 200) {
      // 根据 data.boolean 的值动态决定消息类型
      const messageType = typedResponse.data.boolean ? "warning" : "success"; // boolean 为 false 时为成功，否则为警告

      if (!typedResponse.data.boolean) {
        ElMessage({
          message: typedResponse.msg,
          type: messageType
          // duration: 5 // 显示时长
        });
      } else {
        // 使用 el-message 显示相应类型的消息
        ElMessageBox({
          title: "警告",
          message: `<p style='color:red'>${typedResponse.msg}</p>`, // 显示返回的 msg
          // type: messageType // 动态决定消息类型
          // duration: 3000 // 显示时长
          showCancelButton: true,
          dangerouslyUseHTMLString: true
        });
      }

      // 处理返回的数据，比如显示列表数据等
      console.log("返回的列表数据", typedResponse.data.list);
    } else {
      // 如果响应的 code 不为 200，表示失败
      ElMessage({
        message: typedResponse.msg || "发生未知错误！", // 显示错误信息
        type: "error" // 错误类型的消息
      });
    }
  } catch (error) {
    // 捕获请求失败的错误
    console.error("接口请求失败", error);
    ElMessage({
      message: "请求失败，请稍后再试",
      type: "error"
    });
  }
};
// 动态调整宽度
const drawerWidth = computed(() => {
  if (showSearch.value || showSearchRam.value) {
    return `${window.innerWidth}px`; // 当 showSearch 或 showSearchHurdle 为 true 时，设置宽度为浏览器窗口宽度
  } else {
    return "450px"; // 否则设置为固定宽度
  }
});
// 方法：根据批次关联日期更新预产日期
const updatePreProductionDate = (newBreedingDate: string | null) => {
  if (newBreedingDate) {
    // 批次关联日期 + 150 天为预产日期
    const breedingDateObj = new Date(newBreedingDate);
    breedingDateObj.setDate(breedingDateObj.getDate() + 150); // 预产日期为批次关联日期加 150 天
    drawerProps.value.row.pre_production_date = breedingDateObj.toISOString().split("T")[0]; // 转为 YYYY-MM-DD 格式
  } else {
    drawerProps.value.row.pre_production_date = ""; // 如果清空批次关联日期，预产日期也清空
  }
};
// 方法：清空预产日期时，联动清空批次关联日期
const clearBreedingDate = () => {
  drawerProps.value.row.breeding_date = ""; // 清空批次关联日期
};

// 方法：清空批次关联日期时，联动清空预产日期
const clearPreProductionDate = () => {
  drawerProps.value.row.pre_production_date = ""; // 清空预产日期
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
  console.log("getEweGrass", getEweGrass(newParams));
  return getEweGrass(newParams);
};

const getTableList1 = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getRamGrass", getRamGrass(newParams));

  return getRamGrass(newParams);
};

// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};

const isEditMode = computed(() => {
  // 判断是否是编辑模式
  return drawerProps.value.title === "编辑";
});

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
  showSearchRam.value = false;
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
const changeBreeddate = params => {
  console.log(typeof params);
  // 将初始时间字符串转换为 Date 对象
  const date = new Date(params);
  // 获取初始时间的日期部分
  let day = date.getDate();
  // 增加 150 天
  day += 150;
  // 设置新的日期
  date.setDate(day);
  // 将修改后的 Date 对象转换为字符串
  const newTime = date.toISOString().split("T")[0];
  drawerProps.value.row.pre_production_date = newTime;
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
  margin-top: 15px;
}
.ml-2 {
  margin-top: 15px;
}
.ml-3 {
  margin-top: 0;
}
.el-message {
  z-index: 9999 !important; /* 调整为更高的值 */
}
.el-form-item {
  padding-right: 30px; /* 控制输入框右侧与滚动条之间的空隙 */
}
</style>
