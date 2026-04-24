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
      <el-form-item label="草地基本信息" prop="basic_id">
        <el-input v-model="drawerProps.row.basic_id" type="number" clearable></el-input>
      </el-form-item>

      <!-- 死亡日期 -->
      <el-form-item label="死亡日期" prop="date">
        <el-date-picker
          v-model="drawerProps.row.date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期"
          clearable
        />
      </el-form-item>

      <!-- 年龄 -->
      <el-form-item label="生长周期" prop="age">
        <el-input v-model="drawerProps.row.age" type="number" clearable></el-input>
      </el-form-item>

      <!-- 死亡原因 -->
      <el-form-item label="死亡原因" prop="cause">
        <el-select v-model="drawerProps.row.cause" clearable>
          <el-option v-for="item in DeathCauseType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <!-- 无害化处理 -->
      <el-form-item label="无害化处理" prop="harmless_treatment">
        <el-select v-model="drawerProps.row.harmless_treatment" clearable>
          <el-option v-for="item in DeathHarmless_treatmentType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <!-- 处理时间 -->
      <el-form-item label="处理时间" prop="t_time">
        <el-date-picker
          v-model="drawerProps.row.t_time"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期"
          clearable
        />
      </el-form-item>

      <!-- 处理人 -->
      <el-form-item label="处理人" prop="t_staff">
        <el-input v-model="drawerProps.row.t_staff" clearable></el-input>
      </el-form-item>

      <!-- 创建人员 -->
      <el-form-item label="创建人员" prop="f_staff">
        <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
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

      <!-- 备注 -->
      <el-form-item label="备注" prop="notes">
        <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
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
import {
  colonyFuntionType,
  colonyH_typeType,
  DeathCauseType,
  DeathHarmless_treatmentType,
  manuScaleType,
  manutypeType
} from "@/assets/json/typeListJson";

const rules = reactive({
  basic_id: [
    {
      required: true,
      message: "请填写草地基本信息"
    }
  ],
  date: [
    {
      required: true,
      message: "请填写死亡日期"
    }
  ],
  cause: [
    {
      required: true,
      message: "请填写死亡原因"
    }
  ],
  harmless_treatment: [
    {
      required: true,
      message: "请选择无害化处理方式"
    }
  ],
  t_time: [
    {
      required: true,
      message: "请填写处理时间"
    }
  ],
  t_staff: [
    {
      required: true,
      message: "请填写处理人"
    }
  ],
  notes: [
    {
      required: true,
      message: "请填写备注"
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
