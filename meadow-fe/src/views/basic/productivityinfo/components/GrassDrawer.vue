<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" size="450px" :title="`${drawerProps.title}草地基本信息`">
    <el-form
      ref="ruleFormRef"
      label-width="160px"
      label-suffix=" :"
      :rules="rules"
      :disabled="drawerProps.isView"
      :model="drawerProps.row"
      :hide-required-asterisk="drawerProps.isView"
    >
      <el-form-item label="草地基本信息id" prop="basic_id">
        <el-input v-model="drawerProps.row.basic_id" clearable></el-input>
      </el-form-item>
      <el-form-item label="生物量" prop="weight">
        <el-input v-model.number="drawerProps.row.weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- Height -->
      <el-form-item label="体高" prop="high">
        <el-input v-model.number="drawerProps.row.high" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- Oblique Body Length -->
      <el-form-item label="斜体长" prop="Llong">
        <el-input v-model.number="drawerProps.row.Llong" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- Bust -->
      <el-form-item label="胸围" prop="bust">
        <el-input v-model.number="drawerProps.row.bust" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- Age in Months -->
      <el-form-item label="生长月数" prop="month_age">
        <el-input v-model.number="drawerProps.row.month_age" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- Fecundity ID -->
      <el-form-item label="繁殖力id" prop="fecundity">
        <el-input v-model.number="drawerProps.row.fecundity" type="number" clearable></el-input>
      </el-form-item>

      <!-- Meat Production Performance -->
      <el-form-item label="产肉性能" prop="per_meat">
        <el-input v-model.number="drawerProps.row.per_meat" type="number" clearable></el-input>
      </el-form-item>

      <!-- Milk Production Performance -->
      <el-form-item label="泌乳性高" prop="per_milk">
        <el-input v-model.number="drawerProps.row.per_milk" type="number" tooltip="请输入整数" clearable></el-input>
      </el-form-item>

      <!-- Hair Production Performance -->
      <el-form-item label="产毛性能" prop="per_hair">
        <el-input v-model.number="drawerProps.row.per_hair" type="number" clearable></el-input>
      </el-form-item>

      <!-- Skin Production Performance -->
      <el-form-item label="产皮性能" prop="per_skin">
        <el-input v-model.number="drawerProps.row.per_skin" type="number" clearable></el-input>
      </el-form-item>

      <!-- Growth Rate -->
      <el-form-item label="生长速度" prop="growth_rate">
        <el-input v-model="drawerProps.row.growth_rate" clearable></el-input>
      </el-form-item>

      <!-- Feed Conversion Rate -->
      <el-form-item label="饲料转化率" prop="FCR">
        <el-input v-model.number="drawerProps.row.FCR" type="number" step="0.01" clearable></el-input>
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
import { manuScaleType, manutypeType } from "@/assets/json/typeListJson";

const rules = reactive({
  basic_id: [{ required: true, message: "请输入草地基本信息" }],
  growth_rate: [{ required: true, message: "请输入生长速度" }]
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
      ElMessage.success({ message: `${drawerProps.value.title}产地成功！` });
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
