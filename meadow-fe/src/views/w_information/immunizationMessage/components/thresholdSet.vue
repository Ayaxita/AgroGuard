<template>
  <el-dialog v-model="dialogVisible" title="阈值设置" width="600">
    <el-form
      ref="ruleFormRef"
      label-width="160px"
      label-suffix=" :"
      :disabled="!dialogVisible"
      :hide-required-asterisk="dialogVisible"
    >
      <el-scrollbar height="400px">
        <el-form-item v-for="(data, index) in dialogProps.model_data" :key="index" label-position="top">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>{{ displayImmCname(String(data.cname ?? "")) }}</span>
              </div>
            </template>
            <span class="card-detail">日间阈值 (day)</span>
            <el-radio-group v-model="dialogProps.model_data[index].ifyear">
              <el-radio :value="1" border>全周期仅防护一次</el-radio>
              <el-radio :value="0" border>循环防护</el-radio>
            </el-radio-group>
            <el-slider
              :id="index + 'day'"
              v-model="dialogProps.model_data[index].threshold"
              :max="365"
              :format-tooltip="tooltipTextday"
              @change="handleSliderChange('day', dialogProps.model_data[index])"
              show-input
            />
            <!-- 季度阈值 (month)
            <el-slider
              :id="index + 'mon'"
              v-model="dialogProps.model_data[index].threshold_mon"
              :max="3"
              :format-tooltip="tooltipTextmonth"
              @change="handleSliderChange('mon', dialogProps.model_data[index])"
              show-input
            />
            年度阈值 (year)
            <el-slider
              :id="index + 'year'"
              v-model="dialogProps.model_data[index].threshold_year"
              :max="3"
              :format-tooltip="tooltipTextyear"
              @change="handleSliderChange('year', dialogProps.model_data[index])"
              show-input
            /> -->
          </el-card>
        </el-form-item>

        <!-- <el-form-item label="植保药剂" prop="smallruminant_vaccine" label-position="top">
          日间阈值 (day)
          <el-slider v-model="dialogProps.model_data[0].threshold" :max="90" :format-tooltip="tooltipTextday" show-input />
          季度阈值 (month)
          <el-slider v-model="dialogProps.model_data[0].threshold_mon" :max="9" :format-tooltip="tooltipTextmonth" show-input />
          年度阈值 (year)
          <el-slider v-model="dialogProps.model_data[0].threshold_year" :max="3" :format-tooltip="tooltipTextyear" show-input />
        </el-form-item>
        <el-divider />
        <el-form-item label="真菌病防护剂" prop="footAndmouth_disease" label-position="top">
          日间阈值 (day)
          <el-slider v-model="dialogProps.model_data[1].threshold" :max="365" :format-tooltip="tooltipTextday" show-input />
          季度阈值 (month)
          <el-slider v-model="dialogProps.model_data[1].threshold_mon" :max="9" :format-tooltip="tooltipTextmonth" show-input />
          年度阈值 (year)
          <el-slider v-model="dialogProps.model_data[1].threshold_year" :max="3" :format-tooltip="tooltipTextyear" show-input />
        </el-form-item>
        <el-divider />
        <el-form-item label="锈病防护剂" prop="modified_smallpox" label-position="top">
          日间阈值 (day)
          <el-slider v-model="dialogProps.model_data[2].threshold" :max="90" :format-tooltip="tooltipTextday" show-input />
          季度阈值 (month)
          <el-slider v-model="dialogProps.model_data[2].threshold_mon" :max="9" :format-tooltip="tooltipTextmonth" show-input />
          年度阈值 (year)
          <el-slider v-model="dialogProps.model_data[2].threshold_year" :max="3" :format-tooltip="tooltipTextyear" show-input />
        </el-form-item>
        <el-divider />
        <el-form-item label="综合防护剂" prop="three_links_four_defenses" label-position="top">
          日间阈值 day
          <el-slider v-model="dialogProps.model_data[3].threshold" :max="90" :format-tooltip="tooltipTextday" show-input />
          季度阈值 month
          <el-slider v-model="dialogProps.model_data[3].threshold_mon" :max="9" :format-tooltip="tooltipTextmonth" show-input />
          年度阈值 year
          <el-slider v-model="dialogProps.model_data[3].threshold_year" :max="3" :format-tooltip="tooltipTextyear" show-input />
        </el-form-item>
        <el-divider />
        <el-form-item label="剪毛" prop="cropping" label-position="top">
          日间阈值 day
          <el-slider :max="90" :format-tooltip="tooltipTextday" show-input />
          季度阈值 month
          <el-slider :max="9" :format-tooltip="tooltipTextmonth" show-input />
          年度阈值 year
          <el-slider :max="3" :format-tooltip="tooltipTextyear" show-input /> -->
        <!-- </el-form-item> -->
        <!-- <el-divider /> -->
      </el-scrollbar>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit"> 确认 </el-button>
      </div>
    </template>
  </el-dialog>
</template>
<script setup lang="ts" name="thresholdSet">
import { reactive, ref, watch } from "vue";
import { getThresholdeinfo } from "../api/manu";
import { ElMessage } from "element-plus";

/** 后端返回的防护剂名称在界面上的草地监测用语映射（不改变提交数据） */
const IMM_CNAME_DISPLAY_MAP: Record<string, string> = {
  草地锈病防治剂: "锈病防治剂",
  草地褐斑病杀菌剂: "褐斑病杀菌剂",
  草地蚜虫杀虫剂: "蚜虫杀虫剂",
  草地白粉病防治剂: "白粉病防治剂",
  草地腐霉枯萎病药剂: "腐霉枯萎病药剂",
  草地纹枯病防治剂: "纹枯病防治剂",
  草地螟虫杀虫剂: "螟虫杀虫剂",
  草地综合管理剂: "综合管理剂"
};
const displayImmCname = (cname: string) => IMM_CNAME_DISPLAY_MAP[cname] ?? cname;

const tooltipTextday = value => {
  return String(value) + "天";
};
const tooltipTextmonth = value => {
  return String(value) + "月";
};
const tooltipTextyear = value => {
  return String(value) + "年";
};
interface Immthresholdset {
  id: number;
  vaccine_id: number;
  threshold: number;
  threshold_mon: number;
  threshold_year: number;
  cname: String;
  ifyear: number;
  ifchange: number;
}
interface DialogProps {
  isView: boolean;
  model_data: Array<Immthresholdset>;
  api?: (params: any) => Promise<any>;
  getTableList?: () => void;
}
const dialogVisible = ref(false);
const dialogProps = ref<DialogProps>({
  isView: false,
  model_data: [
    {
      id: -1,
      vaccine_id: -1,
      threshold: -1,
      threshold_mon: -1,
      threshold_year: -1,
      cname: "",
      ifyear: -1,
      ifchange: -1
    },
    {
      id: -1,
      vaccine_id: -1,
      threshold: -1,
      threshold_mon: -1,
      threshold_year: -1,
      cname: "",
      ifyear: -1,
      ifchange: -1
    },
    {
      id: -1,
      vaccine_id: -1,
      threshold: -1,
      threshold_mon: -1,
      threshold_year: -1,
      cname: "",
      ifyear: -1,
      ifchange: -1
    }
  ]
});
const formData = reactive<any>({}); // 存储滑块的数据
// 接收父组件传过来的参数
const acceptParams = (isOpen: boolean, data: DialogProps) => {
  dialogProps.value = data;
  for (let index = 0; index < data.model_data.length; index++) {
    dialogProps.value.model_data[index] = data.model_data[index];
  }
  dialogVisible.value = isOpen;
};
const handleSubmit = async () => {
  try {
    console.log("dialogProps.value.row", dialogProps.value.model_data);
    await dialogProps.value.api!(dialogProps.value.model_data);
    ElMessage.success({ message: `修改阈值成功！` });
    dialogProps.value.getTableList;
    dialogVisible.value = false;
  } catch (error) {
    console.log(error);
  }
};

//处理滑块的变化
function handleSliderChange(sliderType, data) {
  if (sliderType === "day" && data.threshold !== 0) {
    // 当日间滑块有值时，将其他两个滑块值设为 0
    data.threshold_mon = 0;
    data.threshold_year = 0;
  } else if (sliderType === "mon" && data.threshold_mon !== 0) {
    // 当季度滑块有值时，将其他两个滑块值设为 0
    data.threshold = 0;
    data.threshold_year = 0;
  } else if (sliderType === "year" && data.threshold_year !== 0) {
    // 当年度滑块有值时，将其他两个滑块值设为 0
    data.threshold = 0;
    data.threshold_mon = 0;
  }
}
defineExpose({
  acceptParams
});
</script>
<style>
.el-dialog {
  /* stylelint-disable-next-line color-function-notation */
  background-color: rgb(246, 244, 244);
}
.el-radio-group {
  margin-left: 5%;
}
.el-slider {
  width: 90%;
  margin-top: 10%;
  margin-right: 10%;
  margin-left: 5%;
}
.el-card {
  width: 95%;
  height: 250px;
  /* stylelint-disable-next-line color-function-notation */
  background-color: rgb(255, 255, 255);
  .card-header {
    height: 20px;
    font-weight: bolder;
    text-align: left;
  }
}
</style>
