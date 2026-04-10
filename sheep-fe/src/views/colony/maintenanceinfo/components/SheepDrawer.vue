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
      <el-form-item label="监测区域编号" prop="house_id">
        <el-input v-model="drawerProps.row.house_id" clearable></el-input>
      </el-form-item>

      <!-- 维护情况 -->
      <el-form-item label="维护情况" prop="M_condition">
        <el-input v-model="drawerProps.row.M_condition" type="textarea" clearable></el-input>
      </el-form-item>

      <!-- 维修内容 -->
      <el-form-item label="维修内容" prop="M_details">
        <el-input v-model="drawerProps.row.M_details" type="textarea" clearable></el-input>
      </el-form-item>

      <!-- 维护时间 -->
      <el-form-item label="维护时间" prop="M_time">
        <el-date-picker
          v-model="drawerProps.row.M_time"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item>

      <!-- 维护成本 -->
      <el-form-item label="维护成本" prop="M_cost">
        <el-input v-model="drawerProps.row.M_cost" type="number" step="0.01" clearable></el-input>
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
    <template #footer>
      <el-button @click="drawerVisible = false">取消</el-button>
      <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="SheepDrawer">
import { ref, reactive } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { manuScaleType, manutypeType } from "@/assets/json/typeListJson";

const rules = reactive({
  house_id: [
    {
      required: true,
      message: "请填写监测区域编号"
    }
  ],
  M_condition: [
    {
      required: true,
      message: "请填写维护情况"
    }
  ],
  M_details: [
    {
      required: true,
      message: "请填写维修内容"
    }
  ],
  M_time: [
    {
      required: true,
      message: "请选择维护时间"
    }
  ],
  M_cost: [
    {
      required: true,
      message: "请填写维护成本"
    }
  ]
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
