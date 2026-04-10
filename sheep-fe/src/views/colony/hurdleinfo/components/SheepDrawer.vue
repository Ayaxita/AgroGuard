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
      <!-- 棚自动填0 -->
      <!-- <el-form-item label="上级id" prop="pid">
        <el-input v-model="drawerProps.row.pid" clearable></el-input>
      </el-form-item> -->
      <!-- <el-form-item label="监测站点名称" prop="pid">
        <el-input v-model="drawerProps.row.pid" clearable></el-input>
      </el-form-item> -->
      <el-form-item label="监测地块名称" prop="name">
        <el-input v-model="drawerProps.row.name" clearable></el-input>
      </el-form-item>
      <el-form-item label="区域类型" prop="h_type">
        <el-select v-model="drawerProps.row.h_type" clearable>
          <el-option v-for="item in colonyH_typeType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地类型" prop="sheep_type">
        <el-select v-model="drawerProps.row.sheep_type" clearable>
          <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="监测地块功能" prop="function">
        <el-select v-model="drawerProps.row.function" clearable>
          <el-option v-for="item in colonyFuntionType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="监测地块面积(平方米)" prop="area">
        <el-input v-model="drawerProps.row.area" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item label="地块尺寸" prop="h_lwh">
        <el-input v-model="drawerProps.row.h_lwh" clearable></el-input>
      </el-form-item>
      <el-form-item label="生长区尺寸" prop="sports_lwh">
        <el-input v-model="drawerProps.row.sports_lwh" clearable></el-input>
      </el-form-item>
      <!-- 地块数量要从基本表算 -->
      <!-- <el-form-item label="地块数量" prop="sheep_quantity">
        <el-input v-model="drawerProps.row.sheep_quantity" type="number" clearable></el-input>
      </el-form-item> -->
      <!-- 面积比例要算出来 -->
      <!-- <el-form-item label="草地覆盖率" prop="area_pro">
        <el-input v-model="drawerProps.row.area_pro" clearable></el-input>
      </el-form-item> -->

      <!-- 防疫日期在监测地块展示 -->
      <!-- <el-form-item label="防疫日期" prop="difinfect_time">
        <el-date-picker
          v-model="drawerProps.row.difinfect_time"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item> -->
      <el-form-item label="建设时间" prop="build_time">
        <el-date-picker
          v-model="drawerProps.row.build_time"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item>
      <el-form-item label="管理人员" prop="staff">
        <el-input v-model="drawerProps.row.staff" clearable></el-input>
      </el-form-item>
      <!-- 创建人员其实要自动填入，应该是从Pinia里面获取 -->
      <!-- <el-form-item label="创建人员" prop="f_staff">
        <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
      </el-form-item> -->
    </el-form>
    <template #footer>
      <el-button @click="drawerVisible = false">取消</el-button>
      <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="SheepDrawer">
import { ref, reactive, onBeforeMount } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { colonyFuntionType, colonyH_typeType, varietyType } from "@/assets/json/typeListJson";
import { initHouse } from "../api/manu";

const rules = reactive({
  // pid: [{ required: true, message: "请输入上级id" }],
  name: [{ required: true, message: "请输入名称" }],
  build_time: [{ required: true, message: "请输入建设时间" }],
  function: [{ required: true, message: "请选择功能" }],
  h_type: [{ required: true, message: "请选择区域类型" }],
  h_lwh: [{ required: true, message: "请输入区域尺寸" }],
  area: [{ required: true, message: "请输入监测地块面积" }],
  sports_lwh: [{ required: true, message: "请输入生长区尺寸" }],
  area_pro: [{ required: true, message: "请输入草地覆盖率" }],
  staff: [{ required: true, message: "请输入管理人员" }]
});

interface DrawerProps {
  title: string;
  isView: boolean;
  // row: Partial<User.ResUserList>;
  row: any;
  api?: (params: any) => Promise<any>;
  getTableList?: () => void;
}

// const houses = ref<any>([]);

// // 初始化house

// onBeforeMount(() => {
//   initHouse().then((res: any) => {
//     if (res.code === 200) {
//       houses.value = res.data.list;
//     } else {
//       ElMessage.error("获取监测站点列表失败！");
//     }
//   });
// });
const drawerVisible = ref(false);
const drawerProps = ref<DrawerProps>({
  isView: false,
  title: "",
  row: {}
});

// 接收父组件传过来的参数
const acceptParams = (params: DrawerProps) => {
  drawerProps.value = params;
  drawerProps.value.row.pid = drawerProps.value.row.house_id;
  console.log("我是监测站点名称", drawerProps.value.row.house_id);

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
