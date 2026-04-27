<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :size="drawerWidth" :title="`${drawerProps.title}长势监测信息`">
    <div class="drawer-container">
      <div class="left-section" v-if="showSearch">
        <!-- 搜索框 -->
        <!-- <el-form :model="searchParams" class="search-form">
          <el-form-item label="搜索条件" prop="search">
            <el-input v-model="searchParams.search" clearable placeholder="请输入搜索条件" />
          </el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form> -->

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
          <!-- 基本信息id -->
          <el-form-item label="草地编号" prop="ele_num">
            <el-input v-model="drawerProps.row.ele_num" clearable :disabled="isEditMode"></el-input>
            <el-button size="small" type="primary" class="ml-2" @click="toggleSearchTable">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              选择草地信息
            </el-button>
          </el-form-item>
          <el-form-item label="草地类型" prop="variety" v-if="drawerProps.title === '查看'">
            <el-select v-model="drawerProps.row.variety" clearable :disabled="isEditMode">
              <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <!-- 测量日期 -->
          <el-form-item label="测量日期" prop="date">
            <el-date-picker
              v-model="drawerProps.row.date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
            />
          </el-form-item>

          <!-- 生长月数 -->
          <el-form-item label="生长月数" prop="age">
            <el-select v-model="drawerProps.row.age" clearable @change="checkAge">
              <el-option
                v-for="item in breederMonAgeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>

          <!-- 新加生长月数 -->
          <!-- <el-form-item label="生长月数" prop="mon_age">
            <el-select v-model="drawerProps.row.mon_age" clearable>
              <el-option v-for="item in monAgeType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item> -->

          <!-- 草色 -->
          <!-- <el-form-item label="草地颜色" prop="color">
            <el-select v-model="drawerProps.row.color" clearable>
              <el-option v-for="item in colorType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item> -->

          <!-- 外貌等级 -->
          <el-form-item label="外貌等级" prop="rank">
            <el-select v-model="drawerProps.row.rank" clearable>
              <el-option v-for="item in rankType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>

          <!-- 体高 -->
          <el-form-item label="体高" prop="high">
            <el-input v-model="drawerProps.row.high" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 生物量 -->
          <el-form-item label="生物量" prop="weight">
            <el-input v-model="drawerProps.row.weight" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 斜体长 -->
          <el-form-item label="斜体长" prop="Llong">
            <el-input v-model="drawerProps.row.Llong" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 胸围 -->
          <el-form-item label="胸围" prop="bust">
            <el-input v-model="drawerProps.row.bust" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 茎径 -->
          <el-form-item label="茎径" prop="back_fat">
            <el-input v-model="drawerProps.row.back_fat" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 叶面积 -->
          <el-form-item label="叶面积" prop="eye">
            <el-input v-model="drawerProps.row.eye" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 形态指标 -->
          <el-form-item v-if="false" label="形态指标" prop="testis_shape">
            <el-select v-model="drawerProps.row.testis_shape" clearable>
              <el-option
                v-for="item in breederconditioninfo_TestisShapeType"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item>

          <!-- 测量人员 -->
          <el-form-item label="测量人员" prop="t_staff">
            <el-input v-model="drawerProps.row.t_staff" clearable></el-input>
          </el-form-item>

          <!-- 外貌评定 -->
          <el-form-item label="外貌评定" prop="AE">
            <el-input v-model="drawerProps.row.AE" type="textarea" clearable></el-input>
          </el-form-item>

          <!-- 生产性能 -->
          <el-form-item label="生产性能" prop="performance_traits">
            <el-input v-model="drawerProps.row.performance_traits" clearable></el-input>
          </el-form-item>

          <!-- 同批次数 -->
          <el-form-item v-if="false" label="同批次数" prop="with_births">
            <el-input type="number" v-model="drawerProps.row.with_births" clearable :disabled="isEditMode"></el-input>
          </el-form-item>

          <!-- 阶段切换重 -->
          <el-form-item label="阶段生物量" prop="wea_weight">
            <el-input v-model="drawerProps.row.wea_weight" type="number" step="0.01" clearable :disabled="isEditMode"></el-input>
          </el-form-item>

          <!-- 六月生物量 -->
          <el-form-item label="六月生物量" prop="June_heavy">
            <el-input v-model="drawerProps.row.June_heavy" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 健康情况 -->
          <el-form-item label="健康情况" prop="health">
            <el-input v-model="drawerProps.row.health" clearable></el-input>
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

          <!-- 备注 -->
          <el-form-item label="备注" prop="notes">
            <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
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
import { User } from "@/api/interface";
import { breederconditioninfo_TestisShapeType, colorType, rankType, varietyType } from "@/assets/json/typeListJson";

const breederMonAgeOptions = [
  { label: "生长月2", value: 2 },
  { label: "生长月6", value: 6 },
  { label: "生长月12", value: 12 },
  { label: "生长月24", value: 24 }
];
import { getGrassList } from "@/views/basic/basicinfo/api/grass";
import {
  ElDatePicker,
  ElMessage,
  FormInstance,
  ElMessageBox,
  ElForm,
  ElInput,
  ElFormItem,
  ElOption,
  ElSelect
} from "element-plus";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { ChatRound, CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import {
  colonyTransferReasonType,
  Ewe_conditionType,
  Ewe_healthType,
  Lamb_statType,
  VaccineTypeType
} from "@/assets/json/typeListJson";
import ProTable from "@/components/ProTable/index.vue";
import {
  sexType,
  gene_aType,
  gene_bType,
  gene_cType,
  stateType,
  purposeType,
  DeathCauseType,
  DeathHarmless_treatmentType,
  G_harvestTypeType,
  SellingType,
  BooleanType
} from "@/assets/json/typeListJson";
import { getBreederConditionInfoList, getGoodgrass, getWith_births } from "../api/manu";

const rules = reactive({
  date: [{ required: true, message: "请填写测量日期" }],
  basic_id: [{ required: true, message: "请填写草地信息id" }],
  ele_num: [{ required: true, message: "请填写草地信息id" }],
  age: [{ required: true, message: "请填写生长月数" }],
  high: [{ required: true, message: "请填写体高" }],
  weight: [{ required: true, message: "请填写生物量" }],
  Llong: [{ required: true, message: "请填写斜体长" }]
});
// 控制搜索框和表格的显示
const showSearch = ref(false);
// ProTable 列配置
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  {
    prop: "ele_num",
    label: "草地编号",
    search: {
      el: "input"
    }
  },
  // {
  //   prop: "age",
  //   label: "生长月数",
  //   search: {
  //     el: "input"
  //   }
  // },
  // {
  //   prop: "state",
  //   label: "状态",
  //   search: {
  //     el: "input"
  //   }
  // },

  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
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
  }
]);
const toggleSearchTable = () => {
  showSearch.value = !showSearch.value;
};

// 导出列表
const selectEwe = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的记录");
    return;
  } else if (selectedList.length > 1) {
    ElMessageBox.confirm("只能选择1条草地记录?", "温馨提示", { type: "warning" });
    return;
  }
  // 获取选中记录的 ele_num 值

  const selectedEleNum = selectedList[0].ele_num;
  const selectedPreNum = selectedList[0].pre_num;
  const selectedFather = selectedList[0].father_id;
  const selectedMother = selectedList[0].mother_id;
  const selectedFatherelenum = selectedList[0].f_ele_num;
  const selectedMotherelenum = selectedList[0].m_ele_num;
  const selectedWeaweight = selectedList[0].wea_weight;
  const selectedBirth = selectedList[0].birth;
  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedEleNum} 的记录?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    drawerProps.value.row.ele_num = selectedEleNum;
    drawerProps.value.row.pre_num = selectedPreNum;
    drawerProps.value.row.wea_weight = selectedWeaweight;
    if (selectedFatherelenum == "0000000000000000" || selectedMotherelenum == "0000000000000000") {
      //加一行注释吧
      drawerProps.value.row.with_births = null;
    } else {
      const with_births = await getWith_births({
        f_id: selectedFather,
        m_id: selectedMother,
        birth: selectedBirth
      });
      console.log("with_births", with_births);
      drawerProps.value.row.with_births = with_births.data;
    }
    showSearch.value = false;
    ElMessage.success("草地编号已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};
// ProTable 实例引用
const proTable = ref<ProTableInstance>();
// 动态调整宽度
const drawerWidth = computed(() => {
  return showSearch.value ? `${window.innerWidth}px` : "450px";
});

const checkAge = async () => {
  if (drawerProps.value.row.ele_num && drawerProps.value.row.age) {
    const result = await getBreederConditionInfoList({
      ele_num: drawerProps.value.row.ele_num,
      age: drawerProps.value.row.age,
      pageNum: 1,
      pageSize: 10
    });
    console.log("result", result.data);
    if (result.data.list.length != 0) {
      drawerProps.value.row.age = null;
      ElMessageBox.alert("当前记录已在长势监测表中存在，请重新确认信息！");
    }
  } else {
    drawerProps.value.row.age = null;
    ElMessageBox.alert("你应该确保草地编号和生长月数非空");
  }
};
const isEditMode = computed(() => {
  // 判断是否是编辑模式
  return drawerProps.value.title === "编辑";
});
//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getGoodgrass", getGoodgrass(newParams));
  return getGoodgrass(newParams);
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
};

// 提交数据（新增/编辑）
const ruleFormRef = ref<FormInstance>();
const handleSubmit = () => {
  ruleFormRef.value!.validate(async valid => {
    if (!valid) return;
    try {
      console.log("drawerProps.value.row", drawerProps.value.row);
      await drawerProps.value.api!(drawerProps.value.row);
      ElMessage.success({ message: `${drawerProps.value.title}长势监测信息成功！` });
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
.ml-2 {
  margin-top: 15px;
  margin-left: 10px;
}
.el-message {
  z-index: 9999 !important; /* 调整为更高的值 */
}
.el-form-item {
  padding-right: 30px;
}
</style>
