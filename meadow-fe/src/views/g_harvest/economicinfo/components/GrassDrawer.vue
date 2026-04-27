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
      <el-form-item label="草地基本信息ID" prop="basic_id">
        <el-input v-model="drawerProps.row.basic_id" clearable></el-input>
      </el-form-item>
      <el-form-item label="生长年数" prop="age">
        <el-input v-model="drawerProps.row.age" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="圈舍号" prop="house_id">
        <el-input v-model="drawerProps.row.house_id" type="number" clearable></el-input>
      </el-form-item>
      <el-form-item label="入栏体重" prop="in_weight">
        <el-input v-model="drawerProps.row.in_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="入栏1.5月体重" prop="in_1_5">
        <el-input v-model="drawerProps.row.in_1_5" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="入栏3月体重" prop="in_3">
        <el-input v-model="drawerProps.row.in_3" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="入栏4.5月体重" prop="in_4_5">
        <el-input v-model="drawerProps.row.in_4_5" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="出栏体重" prop="out_weight">
        <el-input v-model="drawerProps.row.out_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="投放量（每1.5个月）" prop="put_volume">
        <el-input v-model="drawerProps.row.put_volume" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地投入量（每1.5个月）" prop="intake">
        <el-input v-model="drawerProps.row.intake" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地投入物种类" prop="menu">
        <el-input v-model="drawerProps.row.menu" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="成本" prop="cost">
        <el-input v-model="drawerProps.row.cost" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="草地投入转化效率" prop="FCR">
        <el-input v-model="drawerProps.row.FCR" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="日均增量" prop="ADG">
        <el-input v-model="drawerProps.row.ADG" type="number" step="0.01" clearable></el-input>
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
import { colorType, gene_aType, purposeType, rankType, sexType, stateType, varietyType } from "@/assets/json/typeListJson";
import UploadImg from "@/components/Upload/Img.vue";

const rules = reactive({
  basic_id: [{ required: true, message: "请输入草地基本信息ID" }],
  house_id: [{ required: true, message: "请输入圈舍号" }]
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
