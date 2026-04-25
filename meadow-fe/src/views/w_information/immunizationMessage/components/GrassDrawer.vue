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
      <!-- 其余时间字段 
      <el-form-item label="草地基本信息" prop="basic_id">
        <el-input v-model.number="drawerProps.row.basic_id" type="number" clearable></el-input>
      </el-form-item>
      -->
      <el-form-item label="草地编号" prop="ele_num">
        <el-input v-model.number="drawerProps.row.ele_num" type="string" clearable></el-input>
      </el-form-item>
      <el-form-item label="地块编号" prop="pre_num">
        <el-input v-model.number="drawerProps.row.pre_num" type="string" clearable></el-input>
      </el-form-item>
      <!-- 其余时间字段 -->
      <el-form-item label="接种日期" prop="imm_date">
        <el-date-picker
          v-model="drawerProps.row.imm_date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item>

      <!-- 有小数的输入框 -->
      <el-form-item label="生长月数" prop="imm_age">
        <el-input v-model.number="drawerProps.row.imm_age" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- 没有小数的输入框 -->

      <el-form-item label="防护剂信息" prop="vaccine_id">
        <el-input v-model.number="drawerProps.row.vaccine_id" type="number" clearable></el-input>
      </el-form-item>

      <el-form-item label="防护剂厂家" prop="maker_id">
        <el-input v-model.number="drawerProps.row.maker_id" type="number" clearable></el-input>
      </el-form-item>

      <!-- 备注 -->
      <el-form-item label="操作" prop="operators">
        <el-input v-model="drawerProps.row.operators" type="textarea" clearable></el-input>
      </el-form-item>

      <!-- 类型 -->
      <el-form-item label="剂量" prop="dose">
        <el-input v-model="drawerProps.row.dose" clearable></el-input>
      </el-form-item>

      <el-form-item label="抗病能力监测" prop="anti_level">
        <el-input v-model="drawerProps.row.anti_level" clearable></el-input>
      </el-form-item>

      <el-form-item label="阶段后监测" prop="post_stage">
        <el-input v-model="drawerProps.row.post_stage" clearable></el-input>
      </el-form-item>
      <el-form-item label="出库时间" prop="out_time">
        <el-date-picker
          v-model="drawerProps.row.out_time"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
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
      <!-- 其余字段 -->
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
  // basic_id: [
  //   {
  //     required: true,
  //     message: "请填写草地基本信息"
  //   }
  // ],
  ele_num: [
    {
      required: true,
      message: "请填写草地编号"
    }
  ],
  out_time: [
    {
      required: true,
      message: "请填写出库时间"
    }
  ],
  operators: [
    {
      required: true,
      message: "请填写操作"
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
