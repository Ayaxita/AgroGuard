<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :size="drawerWidth" :title="`${immunizationProps.title}`">
    <div class="drawer-container">
      <div class="left-section" v-if="showCname || showSupplyname">
        <!-- 搜索框 -->
        <!-- <el-form :model="searchParams" class="search-form">
          <el-form-item label="搜索条件" prop="search">
            <el-input v-model="searchParams.search" clearable placeholder="请输入搜索条件" />
          </el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form> -->

        <!-- ProTable -->
        <ProTable
          v-if="showCname"
          ref="proTable"
          :columns="columnsCname"
          :request-api="getCnameList"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectCname(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>
        <ProTable
          v-if="showSupplyname"
          ref="proTable"
          :columns="columnsSupply"
          :request-api="getsupplyTableList"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectSupply(scope.selectedList)">选择</el-button>
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
          :model="immunizationProps"
          :hide-required-asterisk="drawerProps.isView"
        >
          <!-- 其余时间字段 
          <el-form-item label="草地基本信息" prop="basic_id">
            <el-input v-model.number="drawerProps.row.basic_id" type="number" clearable></el-input>
          </el-form-item>
          -->
          <!-- 
          <el-form-item label="草地编号" prop="ele_num">
            <el-input v-model="immunizationProps.ele_num" type="string" clearable></el-input>
          </el-form-item>
          -->
          <!-- 其余时间字段 -->
          <el-form-item label="接种日期" prop="imm_date">
            <el-date-picker
              v-model="immunizationProps.imm_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
            />
          </el-form-item>

          <!-- 有小数的输入框 -->
          <!--
          <el-form-item label="接种生长月数" prop="imm_age">
            <el-input v-model="immunizationProps.imm_age" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          -->
          <!-- 没有小数的输入框 -->

          <el-form-item label="疫苗信息" prop="cname">
            <el-input v-model="immunizationProps.cname" type="string" clearable></el-input>
            <el-button size="small" type="primary" class="ml-2" @click="toggleCnameTable">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              选择疫苗信息
            </el-button>
          </el-form-item>

          <el-form-item label="疫苗厂家" prop="supplier_name">
            <el-input v-model="immunizationProps.supplier_name" type="string" clearable></el-input>
            <el-button size="small" type="primary" class="ml-2" @click="toggleSupplyTable">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              选择厂家信息
            </el-button>
          </el-form-item>

          <!-- 备注 -->
          <el-form-item label="操作" prop="operators">
            <el-input v-model="immunizationProps.operators" type="textarea" clearable></el-input>
          </el-form-item>

          <!-- 类型 -->
          <el-form-item label="剂量" prop="dose">
            <el-input v-model="immunizationProps.dose" clearable></el-input>
          </el-form-item>

          <el-form-item label="防护抗性水平监测" prop="anti_level">
            <el-input v-model="immunizationProps.anti_level" clearable></el-input>
          </el-form-item>

          <el-form-item label="阶段后监测" prop="post_stage">
            <el-input v-model="immunizationProps.post_stage" clearable></el-input>
          </el-form-item>
          <el-form-item label="出库时间" prop="out_time">
            <el-date-picker
              v-model="immunizationProps.out_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
            />
          </el-form-item>
          <el-form-item label="创建时间" prop="f_date">
            <el-date-picker
              v-model="immunizationProps.f_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="创建时间会自动填入"
              disabled
              clearable
            />
          </el-form-item>
          <!-- 其余字段 -->
          <el-form-item label="创建人员" prop="f_staff">
            <el-input v-model="immunizationProps.f_staff" clearable></el-input>
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

<script setup lang="ts" name="immunizationDrawer">
import { ref, reactive, computed } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { ElDatePicker, ElMessageBox, ElForm, ElInput, ElFormItem, ElOption, ElSelect } from "element-plus";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { ChatRound, CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import { VaccineTypeType } from "@/assets/json/typeListJson";
import ProTable from "@/components/ProTable/index.vue";
import { getCnameList } from "@/views/supply/commodityinfo/api/manu";
import { getSupplyList } from "@/views/supply/v_suppliersinfo/api/manu";
import { User } from "@/api/interface";

const immunizationProps = ref<any>({
  title: "新增免疫信息",
  imm_date: null,
  cname: null,
  supplier_name: null,
  operators: null,
  dose: null,
  anti_level: null,
  post_stage: null,
  out_time: null,
  f_date: null,
  f_staff: null
});
// 控制搜索框和表格的显示
const showCname = ref(false);
const showSupplyname = ref(false);
const columnsCname = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  //{ prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "type",
    label: "类别",
    width: 70,
    enum: VaccineTypeType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "cname",
    label: "名称",
    width: 250,
    search: { el: "input" }
  },
  {
    prop: "explain",
    label: "说明",
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
    width: 130,
    search: { el: "input" }
  }
]);
const columnsSupply = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  //{ prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "supplier_name",
    label: "厂商名称",
    search: { el: "input" }
  },
  {
    prop: "sale_type",
    label: "疫苗出售类型",
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
const toggleCnameTable = () => {
  showSupplyname.value = false;
  showCname.value = !showCname.value;
};
const toggleSupplyTable = () => {
  showCname.value = false;
  showSupplyname.value = !showSupplyname.value;
};

// 导出列表
const selectCname = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的疫苗或药品信息");
    return;
  } else if (selectedList.length > 1) {
    ElMessageBox.confirm("只能选择1条信息?", "温馨提示", { type: "warning" });
    return;
  }
  // 获取选中记录的 ele_num 值

  const selectedCname = selectedList[0].cname;
  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择名称为 ${selectedCname} 的信息?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    immunizationProps.value.cname = selectedCname;
    showCname.value = false;
    ElMessage.success("疫苗信息已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};
// 导出列表
const selectSupply = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的厂家信息");
    return;
  } else if (selectedList.length > 1) {
    ElMessageBox.confirm("只能选择1条信息?", "温馨提示", { type: "warning" });
    return;
  }
  // 获取选中记录的 ele_num 值

  const selectedSupply = selectedList[0].supplier_name;
  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择名称为 ${selectedSupply} 的厂家?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    immunizationProps.value.supplier_name = selectedSupply;
    showSupplyname.value = false;
    ElMessage.success("厂家信息已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};
// 动态调整宽度
const drawerWidth = computed(() => {
  return showCname.value || showSupplyname.value ? `${window.innerWidth}px` : "450px";
});
const getcnameTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getCname", getCnameList(newParams));
  return getCnameList(newParams);
};
const getsupplyTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getSupply", getSupplyList(newParams));
  return getSupplyList(newParams);
};
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};
const rules = reactive({
  // basic_id: [
  //   {
  //     required: true,
  //     message: "请填写草地基本信息"
  //   }
  // ],
  ele_num: [
    {
      required: true,
      message: "请填写草地编号"
    }
  ],
  out_time: [
    {
      required: true,
      message: "请填写出库时间"
    }
  ],
  operators: [
    {
      required: true,
      message: "请填写操作"
    }
  ]
});

interface DrawerProps {
  title: string;
  isView: boolean;
  grassList: any[];
  api?: (params: any) => Promise<any>;
  clearSelection?: () => void;
  getTableList?: () => void;
}

const drawerVisible = ref(false);
const drawerProps = ref<DrawerProps>({
  isView: false,
  title: "",
  grassList: []
});

// 接收父组件传过来的参数
const acceptParams = (params: DrawerProps) => {
  drawerProps.value = params;
  drawerVisible.value = true;
};

// 提交数据（新增/编辑）
const ruleFormRef = ref<FormInstance>();
const handleSubmit = () => {
  ruleFormRef.value!.validate(async valid => {
    if (!valid) return;
    try {
      let params = drawerProps.value.grassList.map(item => {
        return {
          ...immunizationProps.value,
          basic_info: item
        };
      });
      //初始化 immunizationProps 表单数据
      ruleFormRef.value?.resetFields();
      console.log("drawerProps.value", drawerProps.value);
      console.log("immunizationProps.value", immunizationProps.value);
      console.log("params.value", params);
      await drawerProps.value.api!(params);
      ElMessage.success({ message: `${drawerProps.value.title}成功！` });
      drawerProps.value.clearSelection!();
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
