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
      <el-form-item label="物资类型" prop="type">
        <el-select v-model="drawerProps.row.type" clearable disabled>
          <el-option v-for="item in InventoryTypeType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="物资名称" prop="goods">
        <el-input v-model="drawerProps.row.goods" clearable disabled></el-input>
      </el-form-item>
      <!-- <el-form-item label="生产厂家id" prop="maker_id">
        <el-input v-model="drawerProps.row.maker_id" clearable></el-input>
      </el-form-item> -->
      <el-form-item label="生产厂家" prop="maker_name">
        <el-input v-model="drawerProps.row.maker_name" clearable disabled></el-input>
      </el-form-item>
      <el-form-item label="库存数量" prop="quantity">
        <el-input v-model="drawerProps.row.quantity" type="number" step="0.01" clearable disabled></el-input>
      </el-form-item>
      <el-form-item label="警戒数量" prop="alert">
        <el-input v-model="drawerProps.row.alert" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="创建时间" prop="f_date">
        <el-date-picker
          v-model="drawerProps.row.f_date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="创建时间会自动填入"
          clearable
        />
      </el-form-item>
      <!-- <el-form-item label="操作" prop="operation">
        <el-input v-model="drawerProps.row.operation" type="textarea" clearable></el-input>
      </el-form-item> -->
      <el-form-item label="创建人员" prop="f_staff">
        <el-input v-model="drawerProps.row.f_staff" clearable disabled></el-input>
      </el-form-item>
      <el-form-item label="更新时间" prop="out_time">
        <el-date-picker
          v-model="drawerProps.row.out_time"
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
import { InventoryTypeType, varietyType } from "@/assets/json/typeListJson";

const rules = reactive({});

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
