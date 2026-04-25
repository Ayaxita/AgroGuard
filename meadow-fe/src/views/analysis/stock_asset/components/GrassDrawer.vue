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
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1">直接费用</el-menu-item>
        <el-menu-item index="0">间接费用</el-menu-item>
      </el-menu>

      <el-form-item v-if="activeIndex == '1'" label="种苗购买费用（元）" prop="buygrass_fees">
        <el-input v-model.number="drawerProps.row.buygrass_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '1'" label="监测检验费用（元）" prop="test_fees">
        <el-input v-model.number="drawerProps.row.test_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '1'" label="人工费用（元）" prop="labor_fees">
        <el-input v-model.number="drawerProps.row.labor_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '1'" label="水电费用（元）" prop="waterEle_fees">
        <el-input v-model.number="drawerProps.row.waterEle_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '1'" label="地租费用（元/年）" prop="land_fees">
        <el-input v-model.number="drawerProps.row.land_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '1'" label="维修费用（元）" prop="maintenance_fees">
        <el-input v-model.number="drawerProps.row.maintenance_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '0'" label="低值易耗品费用（元）" prop="cheep_fees">
        <el-input v-model.number="drawerProps.row.cheep_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '0'" label="管理费用（元）" prop="manage_fees">
        <el-input v-model.number="drawerProps.row.manage_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '0'" label="研发费用（元）" prop="research_fees">
        <el-input v-model.number="drawerProps.row.research_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '0'" label="其他费用（元）" prop="other_fees">
        <el-input v-model.number="drawerProps.row.other_fees" type="number" step="0.01" clearable></el-input>
      </el-form-item>

      <el-form-item v-if="activeIndex == '0'" label="其他费用说明" prop="other_text">
        <el-input v-model="drawerProps.row!.other_text" type="textarea" placeholder="请填写其他费用说明" clearable></el-input>
      </el-form-item>

      <el-form-item label="花费日期" prop="date">
        <el-date-picker
          v-model="drawerProps.row.date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          :disabled="drawerProps.title == '编辑'"
          @change="handleChange"
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
        <el-input v-model="drawerProps.row.f_staff" :disabled="drawerProps.title == '编辑'" clearable></el-input>
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
import { datePickTypes, ElMessage, ElMessageBox, FormInstance } from "element-plus";
import { colonyTransferReasonType, DailyreportType } from "@/assets/json/typeListJson";
import { searchDate } from "../api/manu";

const activeIndex = ref("1");
const handleSelect = (key: string, keyPath: string[]) => {
  activeIndex.value = key;
};
const rules = reactive({
  date: [
    {
      required: true,
      message: "请填写日支出报表花费日期"
    }
  ],
  f_staff: [
    {
      required: true,
      message: "请填写创建人员"
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
  if (params.title === "新增") {
    const fields = [
      "buygrass_fees",
      "test_fees",
      "labor_fees",
      "waterEle_fees",
      "land_fees",
      "maintenance_fees",
      "cheep_fees",
      "manage_fees",
      "research_fees",
      "other_fees"
    ];
    fields.forEach(field => {
      drawerProps.value.row[field] = 0;
    });
    drawerProps.value.row["other_text"] = "";
  }
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
const handleChange = async params => {
  console.log("params", params);
  const dailySheet = await searchDate({ date: params });
  if (dailySheet.msg) {
    ElMessageBox.alert(dailySheet.msg);
  }
};
defineExpose({
  acceptParams
});
</script>
<style scoped>
.el-menu-demo {
  margin-bottom: 20px;
}
</style>
