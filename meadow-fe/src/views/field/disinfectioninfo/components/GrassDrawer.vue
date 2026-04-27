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
      <!-- 监测区域编号 -->
      <el-form-item label="监测区域编号" prop="house_id">
        <el-input v-model="drawerProps.row.house_id" clearable></el-input>
      </el-form-item>

      <!-- 防疫日期 -->
      <el-form-item label="防疫日期" prop="date">
        <el-date-picker
          v-model="drawerProps.row.date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期"
          clearable
        />
      </el-form-item>

      <!-- 防疫人员 -->
      <el-form-item label="防疫人员" prop="staff">
        <el-input v-model="drawerProps.row.staff" clearable></el-input>
      </el-form-item>

      <!-- 防疫药物 -->
      <el-form-item label="防疫药物" prop="drug">
        <el-input v-model="drawerProps.row.drug" clearable></el-input>
      </el-form-item>

      <!-- 稀释比例 -->
      <el-form-item label="稀释比例(重量/平米)" prop="dose">
        <el-input v-model.number="drawerProps.row.dose" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <!-- 防疫方法 -->
      <el-form-item label="防疫方法" prop="method">
        <el-select v-model="drawerProps.row.method" clearable>
          <el-option v-for="item in fieldDisinfectionMethodType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
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

<script setup lang="ts" name="GrassDrawer">
import { ref, reactive } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { fieldDisinfectionMethodType } from "@/assets/json/typeListJson";

const rules = reactive({
  house_id: [
    {
      required: true,
      message: "请输入监测区域编号"
    }
  ],
  date: [
    {
      required: true,
      message: "请输入防疫日期"
    }
  ],
  staff: [
    {
      required: true,
      message: "请输入防疫人员"
    }
  ],
  drug: [
    {
      required: true,
      message: "请输入防疫药物"
    }
  ],
  method: [
    {
      required: true,
      message: "请选择防疫方法"
    }
  ],
  notes: [
    {
      required: true,
      message: "请输入备注"
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
