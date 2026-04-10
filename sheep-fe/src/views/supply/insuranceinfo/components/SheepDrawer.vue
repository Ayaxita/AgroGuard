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
      <!-- 字符串类型字段 -->
      <el-form-item label="保险公司" prop="in_name">
        <el-input v-model="drawerProps.row.in_name" clearable></el-input>
      </el-form-item>
      <el-form-item label="公司电话" prop="contact">
        <el-input v-model="drawerProps.row.contact" clearable></el-input>
      </el-form-item>
      <el-form-item label="公司邮箱" prop="mail">
        <el-input v-model="drawerProps.row.mail" clearable></el-input>
      </el-form-item>
      <el-form-item label="保险理赔员" prop="handler">
        <el-input v-model="drawerProps.row.handler" clearable></el-input>
      </el-form-item>
      <el-form-item label="保险员电话" prop="link">
        <el-input v-model="drawerProps.row.link" clearable></el-input>
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
          :placeholder="`${new Date().getFullYear()}-${new Date().getMonth() + 1}-${new Date().getDate()}`"
          disabled
          clearable
        />
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

const rules = reactive({
  in_name: [{ required: true, message: "请填写保险公司名称" }],
  contact: [{ required: true, message: "请填写公司电话" }],
  // mail: [{ required: true, message: "请填写公司邮箱" }],
  handler: [{ required: true, message: "请填写保险理赔员姓名" }],
  link: [{ required: true, message: "请填写保险员电话" }]
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
