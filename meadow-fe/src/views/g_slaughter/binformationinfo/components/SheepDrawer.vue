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
      <el-form-item label="日期" prop="date">
        <el-date-picker
          v-model="drawerProps.row.date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期"
          clearable
        />
      </el-form-item>
      <el-form-item label="生长周期（月）" prop="month">
        <el-input v-model="drawerProps.row.month" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地基本信息ID" prop="basic_id">
        <el-input v-model="drawerProps.row.basic_id" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地类型" prop="variety">
        <el-select v-model="drawerProps.row.variety" clearable>
          <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地来源" prop="source">
        <el-input v-model="drawerProps.row.source" clearable></el-input>
      </el-form-item>
      <el-form-item label="背膘厚度CM" prop="back_fat_thickness">
        <el-input v-model="drawerProps.row.back_fat_thickness" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="估计净肉率" prop="net_meat_ratio">
        <el-input v-model="drawerProps.row.net_meat_ratio" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="胴体重量" prop="CWT">
        <el-input v-model="drawerProps.row.CWT" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="叶面积Cm^2" prop="emuscle_area">
        <el-input v-model="drawerProps.row.emuscle_area" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="背部厚度" prop="back_thickness">
        <el-input v-model="drawerProps.row.back_thickness" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="级别" prop="level">
        <el-input v-model="drawerProps.row.level" clearable></el-input>
      </el-form-item>
      <el-form-item label="记录员" prop="recorder">
        <el-input v-model="drawerProps.row.recorder" clearable></el-input>
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

<script setup lang="ts" name="SheepDrawer">
import { ref, reactive } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { varietyType } from "@/assets/json/typeListJson";

const rules = reactive({
  date: [{ required: true, message: "请输入日期" }],
  basic_id: [{ required: true, message: "请输入草地基本信息ID" }],
  variety: [{ required: true, message: "请选择草地类型" }],
  source: [{ required: true, message: "请输入草地来源" }],
  level: [{ required: true, message: "请输入级别" }],
  recorder: [{ required: true, message: "请输入记录员" }],
  notes: [{ required: true, message: "请输入备注信息" }]
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
