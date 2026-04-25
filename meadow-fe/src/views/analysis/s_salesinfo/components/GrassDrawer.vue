<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" size="450px" :title="`${drawerProps.title}`">
    <el-form
      ref="ruleFormRef"
      label-width="160px"
      label-suffix=" :"
      :rules="rules"
      :disabled="drawerProps.isView"
      :model="drawerProps.row"
      :hide-required-asterisk="drawerProps.isView"
    >
      <el-form-item label="销售日期" prop="sales_date">
        <el-date-picker
          v-model="drawerProps.row.sales_date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item>
      <el-form-item label="销售单号" prop="sales_order">
        <el-input v-model="drawerProps.row.sales_order" clearable></el-input>
      </el-form-item>
      <el-form-item label="类型" prop="type">
        <el-select v-model="drawerProps.row.type" clearable>
          <el-option v-for="item in G_slaughterTypeType" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="检测编码" prop="quarantine_coding">
        <el-input v-model="drawerProps.row.quarantine_coding" clearable></el-input>
      </el-form-item>
      <el-form-item label="编号" prop="ele_num">
        <el-input v-model="drawerProps.row.ele_num" clearable></el-input>
      </el-form-item>
      <el-form-item label="生长年数" prop="age">
        <el-input v-model.number="drawerProps.row.age" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="是否执行安全间隔期" prop="medical_leave">
        <el-select v-model="drawerProps.row.type" clearable>
          <el-option v-for="item in BooleanType" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="计费单位" prop="billing_unit">
        <el-input v-model="drawerProps.row.billing_unit" clearable></el-input>
      </el-form-item>
      <el-form-item label="单价" prop="unit_price">
        <el-input v-model.number="drawerProps.row.unit_price" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="总价" prop="total_price">
        <el-input v-model.number="drawerProps.row.total_price" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="运输方式" prop="transportation">
        <el-input v-model="drawerProps.row.transportation" clearable></el-input>
      </el-form-item>
      <el-form-item label="销售地点" prop="sales_site">
        <el-input v-model="drawerProps.row.sales_site" type="textarea" clearable></el-input>
      </el-form-item>
      <el-form-item label="销往单位名称" prop="name">
        <el-input v-model="drawerProps.row.name" clearable></el-input>
      </el-form-item>
      <el-form-item label="买方联系人" prop="buyer">
        <el-input v-model="drawerProps.row.buyer" clearable></el-input>
      </el-form-item>
      <el-form-item label="买方电话" prop="buyer_phone">
        <el-input v-model="drawerProps.row.buyer_phone" clearable></el-input>
      </el-form-item>
      <el-form-item label="销往对象类型" prop="selling_type">
        <el-select v-model="drawerProps.row.selling_type" clearable>
          <el-option v-for="item in SellingType" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="备注信息" prop="notes">
        <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
      </el-form-item>
      <el-form-item label="创建人员" prop="f_staff">
        <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="drawerVisible = false">取消</el-button>
      <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="GrassDrawer">
import { ref, reactive } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { BooleanType, G_slaughterTypeType, SellingType } from "@/assets/json/typeListJson";

const rules = reactive({
  sales_date: [{ required: true, message: "请填写销售日期" }],
  sales_order: [{ required: true, message: "请填写销售单号" }],
  type: [{ required: true, message: "请选择类型" }],
  ele_num: [{ required: true, message: "请填写编号" }],
  medical_leave: [{ required: true, message: "请选择是否执行安全间隔期" }],
  billing_unit: [{ required: true, message: "请填写计费单位" }],
  transportation: [{ required: true, message: "请填写运输方式" }],
  sales_site: [{ required: true, message: "请填写销售地点" }],
  name: [{ required: true, message: "请填写销往单位名称" }],
  buyer: [{ required: true, message: "请填写买方联系人" }],
  buyer_phone: [{ required: true, message: "请填写买方电话" }],
  selling_type: [{ required: true, message: "请选择销往对象类型" }],
  notes: [{ required: true, message: "请填写备注信息" }]
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
