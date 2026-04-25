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
      <el-form-item label="厂商名称" prop="supplier_name">
        <el-input v-model="drawerProps.row.supplier_name" clearable></el-input>
      </el-form-item>
      <el-form-item label="防护剂类型" prop="sale_type">
        <el-input v-model="drawerProps.row.sale_type" type="textarea" clearable></el-input>
      </el-form-item>
      <el-form-item label="联系人" prop="sup_linkman">
        <el-input v-model="drawerProps.row.sup_linkman" clearable></el-input>
      </el-form-item>
      <el-form-item label="联系人电话" prop="sup_contact">
        <el-input v-model="drawerProps.row.sup_contact" clearable></el-input>
      </el-form-item>
      <el-form-item label="厂商电话" prop="contact">
        <el-input v-model="drawerProps.row.contact" clearable></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="mail">
        <el-input v-model="drawerProps.row.mail" clearable></el-input>
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input v-model="drawerProps.row.address" clearable></el-input>
      </el-form-item>
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
      <el-form-item label="创建人员" prop="f_staff">
        <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
      </el-form-item>
      <!-- <el-form-item label="操作" prop="operation">
        <el-input v-model="drawerProps.row.operation" type="textarea" clearable></el-input>
      </el-form-item> -->
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
import { FeedingTypeType } from "@/assets/json/typeListJson";

const rules = reactive({
  supplier_name: [{ required: true, message: "请填写厂商名称" }],
  sale_type: [{ required: true, message: "请填写防护剂类型" }],
  sup_linkman: [{ required: true, message: "请填写联系人" }],
  sup_contact: [{ required: true, message: "请填写联系人电话" }],
  address: [{ required: true, message: "请填写地址" }]
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
