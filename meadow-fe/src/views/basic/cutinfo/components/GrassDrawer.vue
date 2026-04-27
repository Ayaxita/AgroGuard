<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :size="drawerWidth" :title="`${drawerProps.title}采收信息`">
    <div class="drawer-container">
      <div class="left-section" v-if="showSearch">
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
          <el-form-item label="监测区域名称" prop="house_name">
            <el-input v-model="drawerProps.row.house_name" clearable :disabled="isEditMode"></el-input>
            <el-button size="small" type="primary" class="ml-2" @click="toggleSearchTable">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              选择监测区域信息
            </el-button>
          </el-form-item>
          <el-form-item label="监测对象数量" prop="ele_quantity">
            <el-input type="number" v-model="drawerProps.row.ele_quantity" clearable :disabled="isEditMode"></el-input>
          </el-form-item>
          <el-form-item label="采收地块数量" prop="cut_num">
            <el-input v-model="drawerProps.row.cut_num" type="number" clearable @change="checkCutnum"></el-input>
          </el-form-item>
          <el-form-item label="采收时间" prop="cut_time">
            <el-date-picker
              v-model="drawerProps.row.cut_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
            />
          </el-form-item>
          <el-form-item label="采收量(kg)" prop="weight">
            <el-input v-model="drawerProps.row.weight" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item label="备注" prop="notes">
            <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
          </el-form-item>
          <el-form-item label="采收人员" prop="staff">
            <el-input v-model="drawerProps.row.staff" clearable></el-input>
          </el-form-item>

          <!-- Select fields -->
          <el-form-item label="草地类型" prop="variety">
            <el-select v-model="drawerProps.row.variety" clearable>
              <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="采收类型" prop="rank">
            <el-select v-model="drawerProps.row.rank" clearable>
              <el-option v-for="item in cutinfoWoolType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="草地颜色" prop="color">
            <el-select v-model="drawerProps.row.color" clearable>
              <el-option v-for="item in colorType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
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
import { colonyFuntionType, colonyH_typeType, cutinfoWoolType } from "@/assets/json/typeListJson";
import { User } from "@/api/interface";
import {
  breederconditioninfo_TestisShapeType,
  colorType,
  rankType,
  varietyType,
  goodgrassAgetype
} from "@/assets/json/typeListJson";
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
import { getHouseList } from "../api/manu";
const rules = reactive({
  house_id: [{ required: true, message: "请输入监测区域编号" }],
  cut_num: [{ required: true, message: "请输入采收地块数量" }],
  cut_time: [{ required: true, message: "请输入采收时间" }],
  staff: [{ required: true, message: "请输入采收人员" }],
  notes: [{ required: true, message: "请输入备注" }]
});

// 控制搜索框和表格的显示
const showSearch = ref(false);
// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
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
    label: "监测区域名称",
    width: 130,
    search: {
      el: "input"
    }
  },
  {
    prop: "function",
    label: "功能",
    width: 120,
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
    label: "监测站点类型",
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
    label: "生长记录区长宽高",
    width: 110,
    search: {
      el: "input"
    }
  },
  {
    prop: "grass_type",
    label: "监测对象类型",
    width: 110,
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "area_pro",
    label: "监测面积比例",
    search: {
      el: "input"
    }
  },
  {
    prop: "grass_quantity",
    label: "监测对象数量",
    search: {
      el: "input",
      props: { type: "number" }
    }
  },
  // {
  //   prop: "difinfect_time",
  //   label: "最后消毒时间",
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
const toggleSearchTable = () => {
  showSearch.value = !showSearch.value;
};
interface InHouseResponse {
  code: number;
  msg: string;
  data: {
    list: any[];
    total: number; // 根据需要，可以更具体地定义 list 的类型
  };
}
const isEditMode = computed(() => {
  // 判断是否是编辑模式
  return drawerProps.value.title === "编辑";
});
// 导出列表
const selectEwe = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的监测区域名称");
    return;
  } else if (selectedList.length > 1) {
    ElMessageBox.confirm("只能选择1个监测区域或监测地块?", "温馨提示", { type: "warning" });
    return;
  }
  // 获取选中记录的 ele_num 值

  const selectedHouse_id = selectedList[0].id;
  const selectedHouse_name = selectedList[0].name;

  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择监测区域名称为 ${selectedHouse_name} ?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    drawerProps.value.row.house_name = selectedHouse_name;
    drawerProps.value.row.house_id = selectedHouse_id;
    if (selectedHouse_name != null) {
      const numGrass = await getGrassList({
        house_name: drawerProps.value.row.house_name,
        state: 1,
        pageNum: 1,
        pageSize: 10
      });
      const typedResponse = numGrass as InHouseResponse;
      drawerProps.value.row.ele_quantity = typedResponse.data.total;
    }
    showSearch.value = false;
    ElMessage.success("监测区域名称已成功添加");
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
//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getGoodgrass", getHouseList(newParams));
  return getHouseList(newParams);
};
// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};

const checkCutnum = () => {
  if (drawerProps.value.row.cut_num > drawerProps.value.row.ele_quantity) {
    drawerProps.value.row.cut_num = null;
    ElMessageBox.alert("采收地块数量不能大于监测区域中总体监测对象数量");
  }
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
      ElMessage.success({ message: `${drawerProps.value.title}采收信息成功！` });
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
