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
      <el-form-item label="草地信息id" prop="basic_id">
        <el-input v-model="drawerProps.row.basic_id" clearable></el-input>
      </el-form-item>

      <el-form-item label="新区域编号" prop="new_house_id">
        <el-input type="number" v-model="drawerProps.row.new_house_id" clearable></el-input>
      </el-form-item>

      <el-form-item label="原区域编号" prop="old_house_id">
        <el-input type="number" v-model="drawerProps.row.old_house_id" clearable></el-input>
      </el-form-item>

      <el-form-item label="转移原因" prop="reason">
        <el-select v-model="drawerProps.row.reason" clearable>
          <el-option v-for="item in colonyTransferReasonType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>

      <el-form-item label="转移时间" prop="trans_time">
        <el-date-picker
          v-model="drawerProps.row.trans_time"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item>

      <el-form-item label="草地类型" prop="grass_type">
        <el-input v-model="drawerProps.row.grass_type" clearable></el-input>
      </el-form-item>

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
import { colonyTransferReasonType } from "@/assets/json/typeListJson";

const rules = reactive({
  basic_id: [
    {
      required: true,
      message: "请填写草地信息id"
    }
  ],
  trans_time: [
    {
      required: true,
      message: "请选择转移时间"
    }
  ],
  grass_type: [
    {
      required: true,
      message: "请填写草地类型"
    }
  ],
  f_date: [
    {
      required: true,
      message: "请确认创建时间"
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
