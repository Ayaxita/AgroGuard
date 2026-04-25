<template>
  <!-- <el-drawer v-model="drawerVisible" :destroy-on-close="true" size="1450px" :title="`${drawerProps.title}`"> -->
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :title="`${drawerProps.title}`" :size="drawerWidth">
    <div class="drawer-container">
      <!-- 左侧：搜索框和表格 -->
      <div class="left-section">
        <!-- 搜索框 -->
        <!-- <el-form :model="searchParams" class="search-form">
          <el-form-item label="搜索条件" prop="search">
            <el-input v-model="searchParams.search" clearable placeholder="请输入搜索条件" />
          </el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form> -->

        <!-- ProTable -->
        <ProTable
          v-if="showSearch"
          ref="proTable"
          :columns="columns"
          :request-api="getTableList"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectEwe(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>
        <ProTable
          v-if="showSearchRam"
          ref="proTable"
          :columns="columns"
          :request-api="getTableList1"
          :data-callback="dataCallback"
          :search-col="4"
        >
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectRam(scope.selectedList)">选择</el-button>
          </template>
          <!-- Expand -->
          <template #expand="scope">
            {{ scope.row }}
          </template>
        </ProTable>
      </div>
      <!-- 右侧：表单内容 -->
      <div
        class="right-section"
        :style="{
          right: drawerVisible ? `${drawerWidth}px` : '0px'
        }"
      >
        <el-form
          ref="ruleFormRef"
          label-width="160px"
          label-suffix=" :"
          :rules="rules"
          :disabled="drawerProps.isView"
          :model="drawerProps.row"
          :hide-required-asterisk="drawerProps.isView"
        >
          <!-- 批次关联信息id -->
          <!-- <el-form-item label="批次关联信息id" prop="breeding_id">
        <el-input v-model="drawerProps.row.breeding_id" type="number" clearable></el-input>
      </el-form-item> -->

          <!-- 批次关联日期 -->
          <!-- <el-form-item label="批次关联日期" prop="breeding_date">
        <el-date-picker
          v-model="drawerProps.row.breeding_date"
          type="date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          placeholder="选择日期时间"
          clearable
        />
      </el-form-item> -->
          <!-- 关联信息编号 -->
          <el-form-item v-if="false" label="关联编号" prop="ewe_ele_num">
            <el-input v-model="drawerProps.row.ewe_ele_num" type="text" clearable :disabled="isEditMode"></el-input>
            <el-button @click="toggleSearchTable" size="small" type="primary" class="ml-2">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              添加关联信息
            </el-button>
          </el-form-item>
          <!-- 收割日期 -->
          <el-form-item label="收割日期" prop="delivery_date">
            <el-date-picker
              v-model="drawerProps.row.delivery_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
              @change="handleDeliveryDateChange"
            />
          </el-form-item>

          <!-- 关联信息编号2 -->
          <el-form-item v-if="false" label="关联编号2" prop="ram_ele_num">
            <el-input v-model="drawerProps.row.ram_ele_num" type="string" clearable :disabled="isEditMode"></el-input>
          </el-form-item>

          <!-- 产量系数 -->
          <el-form-item v-if="false" label="产量系数" prop="Booroola">
            <el-input v-model="drawerProps.row.Booroola" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 健康情况 -->
          <el-form-item v-if="false" label="健康情况" prop="ewe_health">
            <el-select v-model="drawerProps.row.ewe_health" clearable>
              <el-option v-for="item in Ewe_healthType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <!-- 母性情况 -->
          <el-form-item v-if="false" label="母性情况" prop="ewe_condition">
            <el-select v-model="drawerProps.row.ewe_condition" clearable>
              <el-option v-for="item in Ewe_conditionType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>

          <!-- 批次编号 -->
          <!-- <el-form-item label="批次编号" prop="lamb_ele_num">
            <el-input v-model="drawerProps.row.lamb_ele_num" clearable></el-input>
          </el-form-item> -->

          <!-- 批次状态 -->
          <!-- <el-form-item label="批次状态" prop="lamb_state">
            <el-select v-model="drawerProps.row.lamb_state" clearable>
              <el-option v-for="item in Lamb_statType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item> -->

          <!-- 出生生物量 -->
          <!-- <el-form-item label="出生生物量" prop="bir_weight">
            <el-input v-model="drawerProps.row.bir_weight" type="number" step="0.01" clearable></el-input>
          </el-form-item> -->

          <!-- 批次数 -->
          <el-form-item v-if="false" label="批次数" prop="live_num" @change="handleLiveNumChange">
            <el-input v-model="drawerProps.row.live_num" type="number" clearable></el-input>
          </el-form-item>
          <!-- 动态生成的批次信息输入框 -->
          <template v-if="false">
            <div v-for="(lamb, index) in lambs" :key="index">
              <el-card style="margin-right: 5%; margin-bottom: 2%; margin-left: 5%">
                <!-- 批次状态 -->
                <el-form-item :label="'批次 ' + (index + 1) + '状态'" :prop="'state_' + (index + 1)">
                  <el-select v-model="drawerProps.row['state_' + (index + 1)]" clearable>
                    <el-option v-for="item in Lamb_statType" :key="item.value" :label="item.label" :value="item.value" />
                  </el-select>
                </el-form-item>
                <!-- 批次编号 -->
                <el-form-item :label="'批次 ' + (index + 1) + '编号'" :prop="'pre_num_' + (index + 1)">
                  <!-- <el-input v-model="lamb.lamb_ele_num" clearable></el-input> -->
                  <!-- drawerProps.row.live_num，已经尝试了这样写后端能够接收到写在这些输入框中的数据 -->
                  <el-input v-model="drawerProps.row['pre_num_' + (index + 1)]" clearable></el-input>
                </el-form-item>

                <!-- 批次分组 -->
                <el-form-item :label="'批次 ' + (index + 1) + '分组'" :prop="'sex_' + (index + 1)">
                  <el-select v-model="drawerProps.row['sex_' + (index + 1)]" clearable>
                    <el-option v-for="item in sexType" :key="item.value" :label="item.label" :value="item.value" />
                  </el-select>
                </el-form-item>

                <!-- 批次特征 -->
                <el-form-item :label="'批次 ' + (index + 1) + '特征'" :prop="'color_' + (index + 1)">
                  <el-select v-model="drawerProps.row['color_' + (index + 1)]" clearable>
                    <el-option v-for="item in colorType" :key="item.value" :label="item.label" :value="item.value" />
                  </el-select>
                </el-form-item>

                <!-- 批次初始量 -->
                <el-form-item :label="'批次 ' + (index + 1) + '初始量'" :prop="'bir_weight_' + (index + 1)">
                  <el-input v-model="drawerProps.row['bir_weight_' + (index + 1)]" type="number" step="0.01" clearable></el-input>
                </el-form-item>

                <!-- 批次等级 -->
                <el-form-item :label="'批次 ' + (index + 1) + '等级'" :prop="'rank_' + (index + 1)">
                  <el-select v-model="drawerProps.row['rank_' + (index + 1)]" clearable>
                    <el-option v-for="item in rankType" :key="item.value" :label="item.label" :value="item.value" />
                  </el-select>
                </el-form-item>
              </el-card>
            </div>
          </template>

          <!-- 接生人员 -->
          <el-form-item v-if="false" label="采收人员" prop="birth_attendants">
            <el-input v-model="drawerProps.row.birth_attendants" clearable></el-input>
          </el-form-item>

          <!-- 创建人员 -->
          <el-form-item label="创建人员" prop="f_staff">
            <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
          </el-form-item>

          <!-- 创建时间 -->
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

          <!-- 备注 -->
          <el-form-item label="备注" prop="notes">
            <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <!-- 如果 showSearch 为 true，则显示搜索框和表格 -->

    <template #footer>
      <div class="drawer-footer">
        <el-button @click="drawerVisible = false">取消</el-button>
        <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="GrassDrawer">
import { ref, reactive, computed } from "vue";
import { ResultData } from "@/api/interface";
import {
  ElDatePicker,
  ElMessage,
  FormInstance,
  ElMessageBox,
  ElForm,
  ElInput,
  ElFormItem,
  ElOption,
  ElSelect
} from "element-plus";
import { getEwe, searchEweGrass, addBreeding } from "../api/manu";
import { User } from "@/api/interface";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { CirclePlus } from "@element-plus/icons-vue";
import { Ewe_conditionType, Ewe_healthType, Lamb_statType, rankType } from "@/assets/json/typeListJson";
import ProTable from "@/components/ProTable/index.vue";
import { sexType, varietyType, colorType, gene_aType, stateType, purposeType } from "@/assets/json/typeListJson";
import { getRam } from "../../postnatalinfo/api/manu";

const rules = reactive({
  // lamb_ele_num: [
  //   {
  //     required: true,
  //     message: "请填写批次编号"
  //   }
  // ],
  birth_attendants: []
  // notes: [
  //   {
  //     required: true,
  //     message: "请填写备注"
  //   }
  // ]
});

const new_ele = ref<any>(null);
const new_pre = ref<any>(null);
const new_var = ref<any>(null);

// const new_model = computed(() => {
//   return {
//     ele_num: new_ele.value,
//     pre_num: new_pre.value
//   };
// });
const new_model = reactive({
  ele_num: new_ele.value,
  pre_num: new_pre.value,
  variety: new_var.value
});
// 分娩日期变更事件处理
interface GrassData {
  ram_ele_num: string;
  // 如果还需要其他字段，可以在这里扩展
}
const handleDeliveryDateChange = async (newDate: string) => {
  console.log("Selected delivery date:", newDate);
  // 在这里处理日期变更逻辑
  // 准备发送的数据
  const params = {
    deliveryDate: newDate, // 分娩日期
    // 如果需要其他参数，比如记录ID，可以在这里添加
    eweEleNum: drawerProps.value.row.ewe_ele_num // 假设 drawerProps.row.ewe_id 是当前记录的 ID
    //上面那一行刚开始写的时候有错误，经过查询改正，在 Vue 3 中，如果 drawerProps 是一个 ref，你需要通过 drawerProps.value 来访问其内部属性。
  };

  try {
    // 调用更新分娩日期的 API
    const response = await searchEweGrass(params);
    // 假设 response.data 符合 ResultData<GrassData> 类型
    // const data = response.data as ResultData<GrassData>;
    // 使用类型断言来确保我们访问的是正确的字段，我真他吗服了，必须这样才能不标红，上面那种也不行，直接用response.data.ram_ele_num也不行，真傻比
    const data = response.data as ResultData & { ram_ele_num: string }; // 强制认为 data 中直接包含 ram_ele_num

    // 处理响应
    if (data) {
      console.log(response.data);

      ElMessage.success("此记录在培育信息表中有记录，请继续添加");
      // 如果响应成功，填充关联信息编号
      drawerProps.value.row.ram_ele_num = data.ram_ele_num; // 假设后端返回的 ram_ele_num 字段是关联信息编号
    } else {
      // ElMessage.warning("1111");
      ElMessage.warning(response.msg);
      //打开关联信息选择表
      showSearchRam.value = true;
      // 当没有找到相关批次关联记录时，弹出填充关联信息的表单
      ElMessageBox({
        title: "提示",
        message:
          "<p style='color:red'>添加产后信息的关联记录在近期无关联批次记录，请到关联批次信息表中完善该草地信息的关联记录，或在弹出的信息中手动添加关联记录信息</p>",
        showCancelButton: true,
        // customStyle: { color: "red" }
        dangerouslyUseHTMLString: true
      });
    }
  } catch (error) {
    console.log("错误");
    console.log(error);

    console.error("发生错误:", error);
    // ElMessage.error("请在批次关联信息表中添加信息");
  }
};
// 控制搜索框和表格的显示
const showSearch = ref(false);
const showSearchRam = ref(false);
// // 搜索框参数
// const searchParams = reactive({
//   search: ""
// });
// ProTable 列配置
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  {
    prop: "ele_num",
    label: "草地编号",
    width: 150,
    search: {
      el: "input"
    }
  },
  // {
  //   prop: "age",
  //   label: "生长月数",
  //   search: {
  //     el: "input"
  //   }
  // },
  // {
  //   prop: "state",
  //   label: "状态",
  //   search: {
  //     el: "input"
  //   }
  // },

  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
  {
    prop: "pre_num",
    label: "地块编号",
    width: 115,
    search: { el: "input" }
  },
  {
    prop: "purpose",
    label: "用途",
    width: 115,
    enum: purposeType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "variety",
    label: "草地类型",
    width: 100,
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "color",
    label: "草地颜色",
    enum: colorType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "sex",
    label: "作物类型",
    enum: sexType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "birth",
    label: "播种日期",
    width: 110,
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  },
  {
    prop: "wea_date",
    label: "阶段切换日期",
    width: 110,
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  },
  {
    prop: "mon_age",
    label: "生长月数",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "manu_info_name",
    label: "原产地",
    width: 85,
    search: { el: "input" }
  },
  {
    prop: "state",
    label: "状态",
    enum: stateType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "house_name",
    label: "监测区域",
    width: 130,
    search: { el: "input" }
  },
  {
    prop: "hurdle_name",
    label: "监测地块",
    search: { el: "input" }
  },
  {
    prop: "gene_a",
    label: "多批基因",
    enum: gene_aType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  }
]);
// 切换显示搜索框和表格,并搜索符合条件的关联信息
const toggleSearchTable = () => {
  showSearchRam.value = false;
  showSearch.value = !showSearch.value;
};
const toggleSearchRamTable = () => {
  showSearch.value = false;
  showSearchRam.value = !showSearchRam.value;
};
// 导出列表
const selectEwe = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的记录");
    return;
  } else if (selectedList.length > 1) {
    // ElMessageBox.confirm("只能选择1株?", "温馨提示", { type: "warning" });
    ElMessage.warning("只能选择一条记录");
    return;
  }
  // 获取选中记录的 ele_num 值
  const selectedEleNum = selectedList[0].ele_num;

  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedEleNum} 的关联记录?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    drawerProps.value.row.ewe_ele_num = selectedEleNum;

    // 关闭选择表格
    showSearch.value = false;

    ElMessage.success("关联编号已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};
//选择关联信息
const selectRam = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的记录");
    return;
  } else if (selectedList.length > 1) {
    // ElMessageBox.confirm("只能选择1株?", "温馨提示", { type: "warning" });
    ElMessage.warning("只能选择一条记录");
    return;
  }
  // 获取选中记录的 ele_num 值
  const selectedItem = selectedList[0];

  // 确认提示
  try {
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedItem.ele_num} 的记录?`, "温馨提示", {
      type: "warning"
    })
      .then(() => {
        // 获取填写的数据
        const newData = {
          ram_ele_num: selectedItem.ele_num,
          ram_pre_num: selectedItem.pre_num,
          variety: varietyType.find(item => item.value === selectedItem.variety)?.label,
          ewe_ele_num: drawerProps.value.row.ewe_ele_num,
          delivery_date: drawerProps.value.row.delivery_date
        };
        console.log("培育信息的格式", newData);
        // 提交数据到后端
        addBreeding(newData)
          .then(res => {
            if (res.code === 200) {
              // 关闭选择表格
              showSearchRam.value = false;
              ElMessage.success("关联信息添加成功！");
              // 更新当前记录的关联信息编号
              drawerProps.value.row.ram_ele_num = newData.ram_ele_num;
              // // 更新分娩日期为已选择的日期，避免触发日期选择界面
              // drawerProps.value.row.delivery_date = newData.delivery_date;
            } else {
              ElMessage.error("关联信息添加失败！");
            }
          })
          .catch(err => {
            ElMessage.error("提交数据时发生错误");
          });
      })
      .catch(() => {
        ElMessage.warning("您取消了添加关联记录信息");
      });
  } catch (error) {
    console.log("操作取消");
  }
};
// ProTable 实例引用
const proTable = ref<ProTableInstance>();

// 动态调整宽度
const drawerWidth = computed(() => {
  if (showSearch.value || showSearchRam.value) {
    return `${window.innerWidth}px`; // 当 showSearch 或 showSearchHurdle 为 true 时，设置宽度为浏览器窗口宽度
  } else {
    return "450px"; // 否则设置为固定宽度
  }
});

const lambs = ref<any[]>([]);
const numLambs = ref(0);
// 监听批次产出数的变化
const handleLiveNumChange = () => {
  numLambs.value = drawerProps.value.row.live_num; // 获取批次产出数
  console.log("changenumLambs", numLambs.value);
  lambs.value = [];

  // 根据批次产出数生成对应数量的批次信息
  for (let i = 0; i < numLambs.value; i++) {
    lambs.value.push({
      lamb_ele_num: "",
      lamb_state: "",
      lamb_sex: "",
      lamb_color: "",
      lamb_birth_weight: null,
      lamb_grade: ""
    });
    console.log("lambs", lambs);
  }
};
const isEditMode = computed(() => {
  // 判断是否是编辑模式
  return drawerProps.value.title === "编辑";
});
// const drawerWidth = computed(() => (showSearch.value ? "1500px" : "500px"));

//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getEwe", getEwe(newParams));
  return getEwe(newParams);
};
const getTableList1 = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getRam", getRam(newParams));

  return getRam(newParams);
};
// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};

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
  console.log("params", params);
  drawerProps.value = params;
  showSearch.value = false;
  showSearchRam.value = false; //让每次打开抽屉时这些table都处于关闭状态
  console.log("drawerProps.value.row", drawerProps.value.row["list_1"]);
  drawerVisible.value = true;
  showSearch.value = false; // 将 showSearch 设置为 false
  if (drawerProps.value.row.live_num != null) {
    numLambs.value = 0;
    numLambs.value = drawerProps.value.row.live_num;

    // 根据批次产出数生成对应数量的批次信息
    lambs.value = [];
    for (let i = 0; i < numLambs.value; i++) {
      drawerProps.value.row["state_" + (i + 1)] = drawerProps.value.row["list_" + (i + 1)].state;
      drawerProps.value.row["pre_num_" + (i + 1)] = drawerProps.value.row["list_" + (i + 1)].pre_num;
      drawerProps.value.row["sex_" + (i + 1)] = drawerProps.value.row["list_" + (i + 1)].sex;
      drawerProps.value.row["color_" + (i + 1)] = drawerProps.value.row["list_" + (i + 1)].color;
      drawerProps.value.row["bir_weight_" + (i + 1)] = drawerProps.value.row["list_" + (i + 1)].bir_weight;
      drawerProps.value.row["rank_" + (i + 1)] = drawerProps.value.row["list_" + (i + 1)].rank;

      lambs.value.push({
        lamb_ele_num: "",
        lamb_state: "",
        lamb_sex: "",
        lamb_color: "",
        lamb_birth_weight: null,
        lamb_grade: ""
      });
    }
  } else {
    numLambs.value = 0;
    lambs.value = [];
  }

  console.log("numLambs", numLambs.value);
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
<style scoped>
.drawer-container {
  position: relative;
  display: flex;
  height: 100%;
}
.left-section {
  flex: 1;
  max-width: calc(100% - 450px); /* 确保左侧不会挤压右侧 */
  overflow: auto;
  background-color: #f5f5f5; /* 示例背景色，可按需调整 */
}
.right-section {
  position: fixed;
  top: 55px;
  right: 50px;
  width: 400px;
  height: 85vh;
  padding-top: 20px;
  overflow-y: auto;
  background-color: #ffffff;
  box-shadow: -2px 0 5px rgb(0 0 0 / 10%); /* 添加阴影效果 */
}
.drawer-footer {
  position: sticky;
  bottom: 0; /* 固定在底部 */
  z-index: 100; /* 确保在右侧div之上 */
  width: 100%;
  background-color: #ffffff;
}
.ml-2 {
  margin-top: 15px;
  margin-left: 10px;
}
.el-message {
  z-index: 9999 !important; /* 调整为更高的值 */
}
.el-form-item {
  padding-right: 30px; /* 控制输入框右侧与滚动条之间的空隙 */
}
</style>
