<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" size="450px" :title="`${drawerProps.title}草地记录基本信息`">
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
      <el-form-item label="作物类型" prop="sex">
        <el-select v-model="drawerProps.row!.sex" placeholder="请选择作物类型" clearable>
          <el-option v-for="item in sexType" :key="item.value" :label="item.label" :value="item.value" />
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
      <el-form-item label="区段" prop="hurdle_id" v-if="drawerProps.title !== '编辑'">
        <el-select v-model="drawerProps.row!.hurdle_id" filterable placeholder="再选择区段" style="width: 240px">
          <el-option
            v-for="item in drawerProps.house_hurdle_list!.find(item => item.house_id === drawerProps.row.house_id)!?.hurdle_list"
            :key="item.hurdle_id"
            :value="item.hurdle_id"
            :label="item.hurdle_name"
          />
        </el-select>
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
      <el-form-item label="用途" prop="purpose">
        <el-select v-model="drawerProps.row!.purpose" placeholder="请选择用途" clearable>
          <el-option v-for="item in purposeType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地品系" prop="variety">
        <el-select v-model="drawerProps.row!.variety" placeholder="请选择草地品系" clearable>
          <el-option v-for="item in varietyType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="草地颜色" prop="color">
        <el-select v-model="drawerProps.row!.color" placeholder="请选择草地颜色" clearable>
          <el-option v-for="item in colorType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="等级" prop="rank">
        <el-select v-model="drawerProps.row!.rank" placeholder="请选择等级" clearable>
          <el-option v-for="item in rankType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="种植日期" prop="birth">
        <el-date-picker
          v-model="drawerProps.row!.birth"
          type="date"
          placeholder="请选择种植日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
          @change="changedate"
        />
      </el-form-item>
      <el-form-item label="阶段切换日期" prop="wea_date">
        <el-date-picker
          v-model="drawerProps.row!.wea_date"
          type="date"
          placeholder="请选择阶段切换日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
        />
      </el-form-item>
      <el-form-item label="初始生物量" prop="bir_weight">
        <el-input
          v-model="drawerProps.row!.bir_weight"
          placeholder="请填写初始生物量"
          type="number"
          step="0.01"
          clearable
        ></el-input>
      </el-form-item>
      <el-form-item label="生长月数" prop="mon_age">
        <el-input v-model="drawerProps.row!.mon_age" placeholder="请填写生长月数" type="number" step="0.01" clearable></el-input>
      </el-form-item>
      <el-form-item label="阶段生物量" prop="wea_weight">
        <el-input
          v-model="drawerProps.row!.wea_weight"
          placeholder="请填写阶段生物量"
          type="number"
          step="0.01"
          clearable
        ></el-input>
      </el-form-item>
      <el-form-item label="上级地块编号" prop="f_ele_num">
        <el-input v-model="drawerProps.row!.f_ele_num" placeholder="请填写上级地块编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="上级地块编号" prop="f_pre_num">
        <el-input v-model="drawerProps.row!.f_pre_num" placeholder="请填写上级地块编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="当前地块编号" prop="m_ele_num">
        <el-input v-model="drawerProps.row!.m_ele_num" placeholder="请填写当前地块编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="当前地块编号" prop="m_pre_num">
        <el-input v-model="drawerProps.row!.m_pre_num" placeholder="请填写当前地块编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="多批基因" prop="gene_a">
        <el-select v-model="drawerProps.row!.gene_a" placeholder="请选择多批基因" clearable>
          <el-option v-for="item in gene_aType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="抗病基因" prop="gene_b">
        <el-select v-model="drawerProps.row!.gene_b" placeholder="请选择抗病基因" clearable>
          <el-option v-for="item in gene_bType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="待定基因" prop="gene_c">
        <el-select v-model="drawerProps.row!.gene_c" placeholder="请选择待定基因" clearable>
          <el-option v-for="item in gene_cType" :key="item.value" :label="item.label" :value="item.value" />
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
      <el-form-item label="状态" prop="state">
        <el-select v-model="drawerProps.row!.state" placeholder="正常" clearable disabled>
          <el-option v-for="item in stateType" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="备注" prop="note">
        <el-input v-model="drawerProps.row!.note" type="textarea" placeholder="请填写备注" clearable></el-input>
      </el-form-item>
      <el-form-item label="正面照片" prop="img_positive" label-position="left">
        <UploadImg
          v-model:model="drawerProps.row!.img_positive"
          :image-url="
            drawerProps.row!.img_positive && `${BASE_URL}/basic/file/download/img?filename=${drawerProps.row?.img_positive}`
          "
          name="img_positive"
          width="135px"
          height="135px"
          :file-size="3"
          :sheepinfo="drawerProps"
        >
          <template #empty>
            <el-icon><Picture /></el-icon>
            <span>请上传图片</span>
          </template>
          <template #tip> 图片大小不能超过 3M </template>
        </UploadImg>
      </el-form-item>
      <el-form-item label="左侧照片" prop="img_left" label-position="left">
        <UploadImg
          v-model:model="drawerProps.row!.img_left"
          :image-url="drawerProps.row!.img_left && `${BASE_URL}/basic/file/download/img?filename=${drawerProps.row?.img_left}`"
          name="img_left"
          width="135px"
          height="135px"
          :file-size="3"
          :sheepinfo="drawerProps.row"
        >
          <template #empty>
            <el-icon><Picture /></el-icon>
            <span>请上传图片</span>
          </template>
          <template #tip> 图片大小不能超过 3M </template>
        </UploadImg>
      </el-form-item>
      <el-form-item label="右侧照片" prop="img_right" label-position="left">
        <UploadImg
          v-model:model="drawerProps.row!.img_right"
          :image-url="drawerProps.row!.img_right && `${BASE_URL}/basic/file/download/img?filename=${drawerProps.row?.img_right}`"
          name="img_right"
          width="135px"
          height="135px"
          :file-size="3"
          :sheepinfo="drawerProps.row"
        >
          <template #empty>
            <el-icon><Picture /></el-icon>
            <span>请上传图片</span>
          </template>
          <template #tip> 图片大小不能超过 3M </template>
        </UploadImg>
      </el-form-item>
    </el-form>
    <p class="ele_notices" style="color: brown">
      注意：父当前地块编号须是系统中已有，如果是外场引入的草地记录，系统里并无父母信息的记录，则填写“草地编号=0000000000000000，地块编号=00000000000”的草地编号信息，(当前地块编号同样)
    </p>
    <template #footer>
      <el-button @click="drawerVisible = false">取消</el-button>
      <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="SheepDrawer">
import { ref, reactive, watch } from "vue";
// import { genderType } from "@/utils/dict";
import { ElMessage, FormInstance } from "element-plus";
// import { User } from "@/api/interface";
import UploadImg from "@/components/Upload/Img.vue";
import UploadImgs from "@/components/Upload/Imgs.vue";
import {
  sexType,
  rankType,
  varietyType,
  colorType,
  gene_aType,
  gene_bType,
  gene_cType,
  stateType,
  purposeType
} from "@/assets/json/typeListJson";
import { validateSheepNum } from "../api/sheep";

const BASE_URL = import.meta.env.VITE_API_URL;
const validateProps = (rule: any, value: any, callback: any) => {
  if (drawerProps.value.title === "编辑") callback();
  // console.log(rule, value, callback);
  validateSheepNum({
    prop: rule.field,
    value: value
  }).then(res => {
    if (res.realcode === 200) {
      if (rule.field === "f_ele_num") {
        drawerProps.value.row.f_pre_num = res.data!["f_pre_num"];
      } else if (rule.field === "m_ele_num") {
        drawerProps.value.row.m_pre_num = res.data!["m_pre_num"];
      }
      callback();
    } else {
      callback(new Error(res.msg));
    }
  });
};

const rules = reactive({
  // ele_num: [
  //   { required: true, message: "请输入电子耳号", trigger: "blur" },
  //   { validator: validateProps, trigger: "blur" }
  // ],
  pre_num: [
    { required: true, message: "请输入地块编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  f_ele_num: [
    { required: true, message: "请输入上级地块编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  f_pre_num: [
    { required: true, message: "请输入上级地块编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  m_ele_num: [
    { required: true, message: "请输入当前地块编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  m_pre_num: [
    { required: true, message: "请输入当前地块编号", trigger: "blur" },
    { validator: validateProps, trigger: "blur" }
  ],
  house_id: [{ required: true, message: "先选择棚" }],
  hurdle_id: [{ required: true, message: "再选择栏" }],
  birth: [{ required: true, message: "请输入种植日期" }]
});

interface DrawerProps {
  title: string;
  isView: boolean;
  // row: Partial<User.ResUserList>;
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
//改变播种日期自动生成月龄
// 获取今天的日期
const today = new Date();
function changedate() {
  console.log("两个日期");
  console.log(today);
  drawerProps.value.row.mon_age = (getDaysDifference(today, drawerProps.value.row.birth) / 30).toFixed(2); //((drawerProps.value.row.imm_date - selectedBirth) / 30).toFixed(2);
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

// 接收父组件传过来的参数
const acceptParams = (params: DrawerProps) => {
  drawerProps.value = params;
  drawerVisible.value = true;
};
// 改变house后清除hurdle
// 不能直接监听响应式对象的属性，需要一个返回该属性的getter
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
    // console.log("ooooo", drawerProps.value.row.house_name, drawerProps.value.row.hurdle_name);
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

// 提交数据（新增/编辑）
const ruleFormRef = ref<FormInstance>();
const handleSubmit = () => {
  ruleFormRef.value!.validate(async valid => {
    if (!valid) return;
    try {
      console.log("drawerProps.value.row", drawerProps.value.row);
      await drawerProps.value.api!(drawerProps.value.row);
      ElMessage.success({ message: `${drawerProps.value.title}草地记录成功！` });
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
