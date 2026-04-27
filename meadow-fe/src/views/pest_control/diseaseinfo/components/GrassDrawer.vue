<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :title="`${drawerProps.title}`" :size="drawerWidth">
    <div class="drawer-container">
      <div class="left-section" v-if="showSearch">
        <ProTable ref="proTable" :columns="columns" :request-api="getTableList" :data-callback="dataCallback" :search-col="4">
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectEwe(scope.selectedList)">选择</el-button>
          </template>
        </ProTable>
      </div>
      <div class="right-section" :style="{ right: drawerVisible ? `${drawerWidth}px` : '0px' }">
        <el-form
          ref="ruleFormRef"
          label-width="160px"
          label-suffix=" :"
          :rules="rules"
          :disabled="drawerProps.isView"
          :model="drawerProps.row"
          :hide-required-asterisk="drawerProps.isView"
        >
          <el-form-item label="草地编号" prop="ele_num">
            <el-input v-model="drawerProps.row.ele_num" clearable />
            <el-button size="small" type="primary" class="ml-2" @click="toggleSearchTable"> 选择草地信息 </el-button>
          </el-form-item>
          <el-form-item label="发生时间" prop="disease_time">
            <el-date-picker
              v-model="drawerProps.row.disease_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="请选择日期时间"
              clearable
              @change="changeDiseasetime"
            />
          </el-form-item>
          <el-form-item label="生长年数" prop="age">
            <el-input v-model="drawerProps.row.age" type="number" clearable />
          </el-form-item>
          <el-form-item label="病害名称" prop="disease"><el-input v-model="drawerProps.row.disease" clearable /></el-form-item>
          <el-form-item label="处理时间" prop="treatment_time">
            <el-date-picker
              v-model="drawerProps.row.treatment_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="请选择日期时间"
              clearable
            />
          </el-form-item>
          <el-form-item label="处理人员" prop="m_staff"><el-input v-model="drawerProps.row.m_staff" clearable /></el-form-item>
          <el-form-item label="防护药物" prop="cname"><el-input v-model="drawerProps.row.cname" clearable /></el-form-item>
          <el-form-item label="是否合规药物" prop="drug_type">
            <el-select v-model="drawerProps.row.drug_type" clearable>
              <el-option v-for="item in BooleanType" :key="item.value" :label="item.label" :value="item.label" />
            </el-select>
          </el-form-item>
          <el-form-item label="安全间隔期" prop="WDT"><el-input v-model="drawerProps.row.WDT" clearable /></el-form-item>
          <el-form-item label="治疗效果" prop="cur_effect">
            <el-select v-model="drawerProps.row.cur_effect" clearable>
              <el-option v-for="item in d_plantcareCur_effectType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="治愈时间" prop="cur_time">
            <el-date-picker
              v-model="drawerProps.row.cur_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="请选择日期时间"
              clearable
            />
          </el-form-item>
          <el-form-item label="出栏时间" prop="out_time">
            <el-date-picker
              v-model="drawerProps.row.out_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="请选择日期时间"
              clearable
            />
          </el-form-item>
          <el-form-item label="出栏编号" prop="out_no">
            <el-input v-model="drawerProps.row.out_no" type="number" clearable />
          </el-form-item>
          <el-form-item label="创建人员" prop="f_staff"><el-input v-model="drawerProps.row.f_staff" clearable /></el-form-item>
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
import { d_plantcareCur_effectType, BooleanType } from "@/assets/json/typeListJson";
import { User } from "@/api/interface";
import { getGrassList } from "@/views/basic/basicinfo/api/grass";
import { ElMessage, FormInstance, ElMessageBox } from "element-plus";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { CirclePlus } from "@element-plus/icons-vue";
import ProTable from "@/components/ProTable/index.vue";

const rules = reactive({
  disease: [{ required: true, message: "请输入病害名称" }],
  m_staff: [{ required: true, message: "请输入处理人员" }],
  drug_type: [{ required: true, message: "请选择是否合规药物" }],
  WDT: [{ required: true, message: "请输入安全间隔期" }]
});
const showSearch = ref(false);
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "ele_num", label: "草地编号", search: { el: "input" } },
  { prop: "pre_num", label: "地块编号", search: { el: "input" } }
]);
const toggleSearchTable = () => (showSearch.value = !showSearch.value);
let selectedBirth: any;
const selectEwe = async (selectedList: any[]) => {
  if (!selectedList.length) return ElMessage.warning("请选择要添加的草地信息");
  if (selectedList.length > 1) return ElMessage.warning("只能选择 1 条信息");
  const selectedEleNum = selectedList[0].ele_num;
  selectedBirth = selectedList[0].birth;
  try {
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedEleNum} 的记录吗？`, "温馨提示", { type: "warning" });
    drawerProps.value.row.ele_num = selectedEleNum;
    showSearch.value = false;
    ElMessage.success("草地编号添加成功");
  } catch {}
};
const proTable = ref<ProTableInstance>();
const drawerWidth = computed(() => (showSearch.value ? `${window.innerWidth}px` : "450px"));
const getTableList = (params: any) => {
  const p = JSON.parse(JSON.stringify(params));
  p.createTime && (p.startTime = p.createTime[0]);
  p.createTime && (p.endTime = p.createTime[1]);
  delete p.createTime;
  return getGrassList(p);
};
const dataCallback = (data: any) => ({ list: data.list, total: data.total });
interface DrawerProps {
  title: string;
  isView: boolean;
  row: any;
  api?: (params: any) => Promise<any>;
  getTableList?: () => void;
}
const drawerVisible = ref(false);
const drawerProps = ref<DrawerProps>({ isView: false, title: "", row: {} });
const acceptParams = (params: DrawerProps) => {
  drawerProps.value = params;
  drawerVisible.value = true;
  showSearch.value = false;
};
const ruleFormRef = ref<FormInstance>();
const handleSubmit = () => {
  ruleFormRef.value?.validate(async valid => {
    if (!valid) return;
    await drawerProps.value.api?.(drawerProps.value.row);
    ElMessage.success({ message: `${drawerProps.value.title}成功` });
    drawerProps.value.getTableList?.();
    drawerVisible.value = false;
  });
};
function changeDiseasetime() {
  drawerProps.value.row.age = (getDaysDifference(selectedBirth, drawerProps.value.row.disease_time) / 30).toFixed(2);
}
function getDaysDifference(date1: string | Date, date2: string | Date): number {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  return Math.abs((d2.getTime() - d1.getTime()) / (1000 * 3600 * 24));
}
defineExpose({ acceptParams });
</script>

<style scoped>
.drawer-container {
  position: relative;
  display: flex;
  height: 100%;
}
.left-section {
  flex: 1;
  max-width: calc(100% - 450px);
  overflow: auto;
  background-color: #f5f5f5;
}
.right-section {
  position: fixed;
  top: 55px;
  right: 50px;
  width: 400px;
  height: 85vh;
  padding-top: 20px;
  overflow-y: auto;
  background-color: #fff;
  box-shadow: -2px 0 5px rgb(0 0 0 / 10%);
}
.drawer-footer {
  position: sticky;
  bottom: 0;
  z-index: 100;
  width: 100%;
  background-color: #fff;
}
.ml-2 {
  margin-top: 15px;
  margin-left: 10px;
}
.el-form-item {
  padding-right: 30px;
}
</style>
