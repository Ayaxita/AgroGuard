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
      <el-form-item label="草地来源" prop="source">
        <el-input v-model="drawerProps.row.source" clearable></el-input>
      </el-form-item>
      <el-form-item label="创建人员" prop="f_staff">
        <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
      </el-form-item>

      <!-- FloatField -->
      <el-form-item label="生长年数" prop="age">
        <el-input v-model="drawerProps.row.age" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="入场体重" prop="in_weight">
        <el-input v-model="drawerProps.row.in_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="胴体重" prop="CWT">
        <el-input v-model="drawerProps.row.CWT" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="净肉重量" prop="net_meat_weight">
        <el-input v-model="drawerProps.row.net_meat_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="主茎段" prop="spine">
        <el-input v-model="drawerProps.row.spine" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="侧枝段重量" prop="chops_weight">
        <el-input v-model="drawerProps.row.chops_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="髓茎段重量" prop="stick_bone_weight">
        <el-input v-model="drawerProps.row.stick_bone_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="杂骨重量" prop="others_weight">
        <el-input v-model="drawerProps.row.others_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="冠部重量" prop="head_weight">
        <el-input v-model="drawerProps.row.head_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="汁液重量" prop="blood_weight">
        <el-input v-model="drawerProps.row.blood_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="地表覆盖物重量" prop="skin_weight">
        <el-input v-model="drawerProps.row.skin_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="心脏重量" prop="heart_weight">
        <el-input v-model="drawerProps.row.heart_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="肝脏重量" prop="liver_weight">
        <el-input v-model="drawerProps.row.liver_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="肺脏重量" prop="lungs_weight">
        <el-input v-model="drawerProps.row.lungs_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="果腔重量" prop="tripe_weight">
        <el-input v-model="drawerProps.row.tripe_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="基部重量" prop="hoof_weight">
        <el-input v-model="drawerProps.row.hoof_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="粗维管段重量" prop="L_intestine_weight">
        <el-input v-model="drawerProps.row.L_intestine_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="细维管段重量" prop="S_intestine_weight">
        <el-input v-model="drawerProps.row.S_intestine_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="肾脏重量" prop="kidney_weight">
        <el-input v-model="drawerProps.row.kidney_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="髓质重量" prop="white_weight">
        <el-input v-model="drawerProps.row.white_weight" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- DateField -->
      <el-form-item label="登记时间" prop="date">
        <el-date-picker
          v-model="drawerProps.row.date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
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
  basic_id: [{ required: true, message: "请填写草地基本信息ID" }],
  source: [{ required: true, message: "请填写草地来源" }],
  date: [{ required: true, message: "请填写登记时间" }]
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
