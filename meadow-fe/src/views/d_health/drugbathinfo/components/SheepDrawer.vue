<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :title="`${drawerProps.title}`" :size="drawerWidth">
    <div class="drawer-container">
      <div v-if="showSearch || showCname || showSupplyname" class="left-section">
        <ProTable v-if="showSearch" :columns="columns" :request-api="getTableList" :data-callback="dataCallback" :search-col="4">
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectEwe(scope.selectedList)">选择</el-button>
          </template>
        </ProTable>
        <ProTable
          v-if="showCname"
          :columns="columnsCname"
          :request-api="getcnameTableList"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectCname(scope.selectedList)">选择</el-button>
          </template>
        </ProTable>
        <ProTable
          v-if="showSupplyname"
          :columns="columnsSupply"
          :request-api="getsupplyTableList"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectSupply(scope.selectedList)">选择</el-button>
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
            <el-button size="small" type="primary" class="ml-2" @click="toggleSearchTable">选择草地信息</el-button>
          </el-form-item>
          <el-form-item label="药品信息" prop="cname">
            <el-input v-model="drawerProps.row.cname" clearable />
            <el-button size="small" type="primary" class="ml-2" @click="toggleCnameTable">选择药品信息</el-button>
          </el-form-item>
          <el-form-item label="药品厂家" prop="supplier_name">
            <el-input v-model="drawerProps.row.supplier_name" clearable />
            <el-button size="small" type="primary" class="ml-2" @click="toggleSupplyTable">选择厂家信息</el-button>
          </el-form-item>
          <el-form-item label="用药时间" prop="take_time">
            <el-date-picker
              v-model="drawerProps.row.take_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="请选择日期时间"
              clearable
              @change="changeTaketime"
            />
          </el-form-item>
          <el-form-item label="用药生长月数" prop="drug_age">
            <el-input v-model="drawerProps.row.drug_age" type="number" step="0.01" clearable />
          </el-form-item>
          <el-form-item label="作用" prop="effect">
            <el-input v-model="drawerProps.row.effect" type="textarea" clearable />
          </el-form-item>
          <el-form-item label="防护有效期" prop="timing">
            <el-input v-model="drawerProps.row.timing" clearable />
          </el-form-item>
          <el-form-item label="防虫防护处理" prop="IR_bath">
            <el-input v-model="drawerProps.row.IR_bath" clearable />
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
          <el-form-item label="操作员" prop="operators"><el-input v-model="drawerProps.row.operators" clearable /></el-form-item>
          <el-form-item label="创建时间" prop="f_date">
            <el-date-picker
              v-model="drawerProps.row.f_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="创建时间会自动写入"
              disabled
              clearable
            />
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

<script setup lang="ts" name="SheepDrawer">
import { ref, reactive, computed } from "vue";
import { User } from "@/api/interface";
import { getSheepList } from "@/views/basic/basicinfo/api/sheep";
import { ElMessage, FormInstance, ElMessageBox } from "element-plus";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { CirclePlus } from "@element-plus/icons-vue";
import ProTable from "@/components/ProTable/index.vue";
import { VaccineTypeType } from "@/assets/json/typeListJson";
import { getCnameList } from "@/views/supply/commodityinfo/api/manu";
import { getSupplyList } from "@/views/supply/v_suppliersinfo/api/manu";

const rules = reactive({
  out_time: [{ required: true, message: "请填写出栏时间" }],
  operators: [{ required: true, message: "请填写操作员信息" }]
});
const showSearch = ref(false);
const showCname = ref(false);
const showSupplyname = ref(false);
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "ele_num", label: "草地编号", search: { el: "input" } },
  { prop: "pre_num", label: "地块编号", search: { el: "input" } }
]);
const columnsCname = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  {
    prop: "type",
    label: "类别",
    enum: VaccineTypeType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  { prop: "cname", label: "名称", search: { el: "input" } }
]);
const columnsSupply = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "supplier_name", label: "厂家名称", search: { el: "input" } },
  { prop: "contact", label: "厂家电话", search: { el: "input" } }
]);
const toggleSearchTable = () => {
  showCname.value = false;
  showSupplyname.value = false;
  showSearch.value = !showSearch.value;
};
const toggleCnameTable = () => {
  showSearch.value = false;
  showSupplyname.value = false;
  showCname.value = !showCname.value;
};
const toggleSupplyTable = () => {
  showSearch.value = false;
  showCname.value = false;
  showSupplyname.value = !showSupplyname.value;
};
let selectedBirth: any;
const selectEwe = async (selectedList: any[]) => {
  if (!selectedList.length) return ElMessage.warning("请选择要添加的草地信息");
  if (selectedList.length > 1) return ElMessage.warning("只能选择 1 条信息");
  drawerProps.value.row.ele_num = selectedList[0].ele_num;
  selectedBirth = selectedList[0].birth;
  showSearch.value = false;
};
const selectCname = async (selectedList: any[]) => {
  if (!selectedList.length) return ElMessage.warning("请选择药品信息");
  drawerProps.value.row.cname = selectedList[0].cname;
  showCname.value = false;
};
const selectSupply = async (selectedList: any[]) => {
  if (!selectedList.length) return ElMessage.warning("请选择厂家信息");
  drawerProps.value.row.supplier_name = selectedList[0].supplier_name;
  showSupplyname.value = false;
};
const proTable = ref<ProTableInstance>();
const drawerWidth = computed(() =>
  showSearch.value || showCname.value || showSupplyname.value ? `${window.innerWidth}px` : "450px"
);
const normalize = (params: any) => {
  const p = JSON.parse(JSON.stringify(params));
  p.createTime && (p.startTime = p.createTime[0]);
  p.createTime && (p.endTime = p.createTime[1]);
  delete p.createTime;
  return p;
};
const getTableList = (params: any) => getSheepList(normalize(params));
const getcnameTableList = (params: any) => getCnameList(normalize(params));
const getsupplyTableList = (params: any) => getSupplyList(normalize(params));
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
function changeTaketime() {
  drawerProps.value.row.drug_age = (getDaysDifference(selectedBirth, drawerProps.value.row.take_time) / 30).toFixed(2);
}
function getDaysDifference(date1: string | Date, date2: string | Date): number {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  return Math.abs((d2.getTime() - d1.getTime()) / (1000 * 3600 * 24));
}
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
