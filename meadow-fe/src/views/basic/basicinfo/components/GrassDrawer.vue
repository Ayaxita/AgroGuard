<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" size="450px" :title="`${drawerProps.title}草地信息`">
    <el-form
      ref="ruleFormRef"
      label-width="100px"
      label-suffix=" :"
      :rules="rules"
      :disabled="drawerProps.isView"
      :model="drawerProps.row"
      :hide-required-asterisk="drawerProps.isView"
    >
      <el-form-item label="草地编号" prop="ele_num">
        <el-input v-model="drawerProps.row!.ele_num" placeholder="请填写草地编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="地块编号" prop="pre_num">
        <el-input v-model="drawerProps.row!.pre_num" placeholder="请填写地块编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="用途" prop="purpose">
        <el-select v-model="drawerProps.row!.purpose" placeholder="请选择用途" clearable>
          <el-option v-for="item in purposeType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地类型" prop="variety">
        <el-select v-model="drawerProps.row!.variety" placeholder="请选择草地类型" clearable>
          <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地颜色" prop="color">
        <el-select v-model="drawerProps.row!.color" placeholder="请选择草地颜色" clearable>
          <el-option v-for="item in colorType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="作物类型" prop="sex">
        <el-select v-model="drawerProps.row!.sex" placeholder="请选择作物类型" clearable>
          <el-option v-for="item in sexType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="播种日期" prop="birth">
        <el-date-picker
          v-model="drawerProps.row!.birth"
          type="date"
          placeholder="请选择播种日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
          @change="changedate"
        />
      </el-form-item>
      <el-form-item label="阶段结束日期" prop="wea_date">
        <el-date-picker
          v-model="drawerProps.row!.wea_date"
          type="date"
          placeholder="请选择阶段结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
        />
      </el-form-item>
      <el-form-item label="生长月数" prop="mon_age">
        <el-input v-model="drawerProps.row!.mon_age" placeholder="请填写生长月数" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="原产地" prop="manu_info_id">
        <el-select v-model="drawerProps.row!.manu_info_id" filterable placeholder="请选择原产地" style="width: 240px">
          <el-option
            v-for="item in drawerProps.manu_list"
            :key="item.manu_info_id"
            :value="item.manu_info_id"
            :label="item.manu_info_name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="state">
        <el-select v-model="drawerProps.row!.state" placeholder="正常" clearable disabled>
          <el-option v-for="item in stateType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="所属监测区域" prop="house_id" v-if="drawerProps.title !== '编辑'">
        <el-select v-model="drawerProps.row!.house_id" filterable placeholder="先选择监测区域" style="width: 240px">
          <el-option
            v-for="item in drawerProps.house_hurdle_list"
            :key="item.house_id"
            :value="item.house_id"
            :label="item.house_name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="监测地块" prop="hurdle_id" v-if="drawerProps.title !== '编辑'">
        <el-select v-model="drawerProps.row!.hurdle_id" filterable placeholder="请选择监测地块" style="width: 240px">
          <el-option
            v-for="item in drawerProps.house_hurdle_list!.find(item => item.house_id === drawerProps.row.house_id)!?.hurdle_list"
            :key="item.hurdle_id"
            :value="item.hurdle_id"
            :label="item.hurdle_name"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="抗疫基因" prop="gene_a">
        <el-select v-model="drawerProps.row!.gene_a" placeholder="请选择抗疫基因" clearable>
          <el-option v-for="item in gene_aType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="添加人" prop="f_staff">
        <el-input v-model="drawerProps.row!.f_staff" placeholder="请填写添加人" clearable></el-input>
      </el-form-item>
      <el-form-item label="添加时间" prop="f_date">
        <el-date-picker
          v-model="drawerProps.row!.f_date"
          type="date"
          :placeholder="`${new Date().getFullYear()}-${new Date().getMonth() + 1}-${new Date().getDate()}`"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
        />
      </el-form-item>
    </el-form>
    <p class="ele_notices" style="color: brown">
      注意：编号字段需与系统数据保持一致，历史兼容字段由系统内部使用，请按当前业务编号规范填写。
    </p>
    <template #footer>
      <el-button @click="drawerVisible = false">取消</el-button>
      <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="GrassDrawer">
import { ref, reactive, watch } from "vue";
import { ElMessage, FormInstance } from "element-plus";
import { sexType, varietyType, colorType, gene_aType, stateType, purposeType } from "@/assets/json/typeListJson";
import { validateGrassNum } from "../api/grass";

const validateProps = (rule: any, value: any, callback: any) => {
  if (drawerProps.value.title === "编辑") callback();
  validateGrassNum({
    prop: rule.field,
    value: value
  }).then(res => {
    if (res.realcode === 200) {
      callback();
    } else {
      callback(new Error(res.msg));
    }
  });
};

const rules = reactive({
  ele_num: [
    { required: true, message: "请输入草地编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  pre_num: [
    { required: true, message: "请输入地块编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  house_id: [{ required: true, message: "先选择监测区域" }],
  hurdle_id: [{ required: true, message: "请选择监测地块" }],
  birth: [{ required: true, message: "请输入播种日期" }]
});

interface DrawerProps {
  title: string;
  isView: boolean;
  row: any;
  house_hurdle_list?: {
    house_id: number;
    house_name: string;
    hurdle_list: {
      hurdle_id: number;
      hurdle_name: string;
    }[];
  }[];
  manu_list?: {
    manu_info_id: number;
    manu_info_name: string;
  }[];
  api?: (params: any) => Promise<any>;
  getTableList?: () => void;
}

const today = new Date();
function changedate() {
  drawerProps.value.row.mon_age = (getDaysDifference(today, drawerProps.value.row.birth) / 30).toFixed(2);
}
function getDaysDifference(date1: string | Date, date2: string | Date): number {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  return Math.abs((d2.getTime() - d1.getTime()) / (1000 * 3600 * 24));
}

const drawerVisible = ref(false);
const drawerProps = ref<DrawerProps>({
  isView: false,
  title: "",
  row: {}
});

const acceptParams = (params: DrawerProps) => {
  drawerProps.value = params;
  drawerVisible.value = true;
};

watch(
  () => drawerProps.value.row.house_id,
  () => {
    drawerProps.value.row.hurdle_id = null;
  }
);
watch(
  () => drawerProps.value.row.hurdle_id,
  () => {
    drawerProps.value.row.house_name = drawerProps.value.house_hurdle_list!.find(
      item => item.house_id === drawerProps.value.row.house_id
    )?.house_name;
    drawerProps.value.row.hurdle_name = drawerProps.value
      .house_hurdle_list!.find(item => item.house_id === drawerProps.value.row.house_id)
      ?.hurdle_list.find(item => item.hurdle_id === drawerProps.value.row.hurdle_id)?.hurdle_name;
  }
);
watch(
  () => drawerProps.value.row.manu_info_id,
  () => {
    drawerProps.value.row.manu_info_name = drawerProps.value.manu_list!.find(
      item => item.manu_info_id === drawerProps.value.row.manu_info_id
    )?.manu_info_name;
  }
);

const ruleFormRef = ref<FormInstance>();
const handleSubmit = () => {
  ruleFormRef.value!.validate(async valid => {
    if (!valid) return;
    try {
      await drawerProps.value.api!(drawerProps.value.row);
      ElMessage.success({ message: `${drawerProps.value.title}草地信息成功！` });
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

<style scoped>
.ele_notices {
  font-size: 14px;
  color: #606266;
}
</style>
