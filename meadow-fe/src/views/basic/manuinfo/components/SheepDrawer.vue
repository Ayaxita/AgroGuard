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
      <el-form-item label="厂家名称" prop="manu_name">
        <el-input v-model="drawerProps.row!.manu_name" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地规模" prop="scale">
        <el-select v-model="drawerProps.row!.scale" clearable>
          <el-option v-for="item in manuScaleType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地类型" prop="type">
        <el-select v-model="drawerProps.row!.type" clearable>
          <el-option v-for="item in manutypeType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="种植经营许可证编号" prop="BP_license_num">
        <el-input v-model="drawerProps.row!.BP_license_num" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地防疫合格证编号" prop="AP_certificate_num">
        <el-input v-model="drawerProps.row!.AP_certificate_num" clearable></el-input>
      </el-form-item>
      <el-form-item label="营业执照编号" prop="BL_num">
        <el-input v-model="drawerProps.row!.BL_num" clearable></el-input>
      </el-form-item>
      <el-form-item label="法人" prop="legal">
        <el-input v-model="drawerProps.row!.legal" clearable></el-input>
      </el-form-item>
      <el-form-item label="地址" prop="address">
        <el-input v-model="drawerProps.row!.address" clearable></el-input>
      </el-form-item>
      <el-form-item label="联系方式" prop="contact">
        <el-input v-model="drawerProps.row!.contact" clearable></el-input>
      </el-form-item>
      <el-form-item label="所属省" prop="province">
        <el-input v-model="drawerProps.row!.province" clearable></el-input>
      </el-form-item>
      <el-form-item label="市/县" prop="city">
        <el-input v-model="drawerProps.row!.city" clearable></el-input>
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
  manu_name: [{ required: true, message: "请上传用户头像" }],
  scale: [{ required: true, message: "请上传用户照片" }],
  type: [{ required: true, message: "请填写用户姓名" }],
  BP_license_num: [{ required: false, message: "请选择作物类型" }],
  AP_certificate_num: [{ required: false, message: "请选择作物类型" }],
  BL_num: [{ required: false, message: "请填写身份证号" }],
  legal: [{ required: false, message: "请填写邮箱" }],
  address: [{ required: false, message: "请填写邮箱" }],
  contact: [{ required: false, message: "请填写邮箱" }],
  province: [{ required: false, message: "请填写邮箱" }],
  city: [{ required: false, message: "请填写邮箱" }]
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
