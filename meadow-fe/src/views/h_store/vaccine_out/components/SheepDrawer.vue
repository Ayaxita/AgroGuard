<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :size="drawerWidth" :title="`${drawerProps.title}`">
    <div class="drawer-container">
      <div class="left-section" v-if="showSearch">
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
      </div>
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
          <p class="p1" style="color: red">注意！物资名称、物资类型、厂家信息，提交后不能修改</p>

          <el-form-item label="出库时间" prop="delivery_time">
            <el-date-picker
              v-model="drawerProps.row.delivery_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期时间"
              clearable
              @change="Changedelivery_time"
            ></el-date-picker>
          </el-form-item>
          <el-form-item label="出库单号" prop="outbound_no">
            <el-input v-model="drawerProps.row.outbound_no" clearable></el-input>
          </el-form-item>
          <el-form-item label="类别" prop="type">
            <el-select
              v-model="drawerProps.row.type"
              clearable
              :disabled="drawerProps.title === '编辑' || drawerProps.title === '新增'"
            >
              <el-option v-for="item in VaccineTypeType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="农药信息" prop="v_name">
            <el-input
              v-model="drawerProps.row.v_name"
              clearable
              :disabled="drawerProps.title === '编辑' || drawerProps.title === '新增'"
            ></el-input>
            <el-button
              size="small"
              type="primary"
              class="ml-2"
              @click="toggleSearchTable"
              :disabled="drawerProps.title === '编辑'"
            >
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              选择已有防护剂信息
            </el-button>
          </el-form-item>
          <el-form-item label="生产厂家" prop="maker_name">
            <el-input
              v-model.trim="drawerProps.row.maker_name"
              clearable
              :disabled="drawerProps.title === '编辑' || drawerProps.title === '新增'"
            ></el-input>
          </el-form-item>
          <!-- <el-form-item>
            <el-button class="button1" type="primary" plain @click="openAddWindow" v-if="drawerProps.title === '新增'">
              单机弹出添加框
            </el-button>
            <el-button
              class="button2"
              type="primary"
              plain
              @click="drawerProps.row.maker_name = null"
              v-if="drawerProps.title === '新增'"
            >
              取消选择
            </el-button>
          </el-form-item> -->
          <el-form-item label="成分类型" prop="ingredientsType">
            <el-select
              v-model="drawerProps.row.ingredientsType"
              clearable
              :disabled="drawerProps.title === '编辑' || drawerProps.title === '新增'"
            >
              <el-option v-for="item in ingredientsType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <p class="p1" style="color: red">出库数量在填入生产厂家，名称和类型后才能填入</p>

          <el-form-item label="出库数量" prop="num">
            <el-input
              type="number"
              v-model="drawerProps.row.num"
              placeholder="先填入生产厂家，名称和类型"
              clearable
              :disabled="
                !(
                  drawerProps.row.maker_name &&
                  drawerProps.row.v_name &&
                  (drawerProps.row.type === 0 || drawerProps.row.type === 1)
                )
              "
              @input="handleInput"
            ></el-input>
          </el-form-item>

          <el-form-item label="出库用途" prop="out_purposes">
            <el-input v-model="drawerProps.row.out_purposes" type="textarea" clearable></el-input>
          </el-form-item>
          <el-form-item label="出库人员" prop="out_staff">
            <el-input v-model="drawerProps.row.out_staff" clearable></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="contact_phone">
            <el-input v-model="drawerProps.row.contact_phone" clearable></el-input>
          </el-form-item>
          <el-form-item label="备注信息" prop="notes">
            <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
          </el-form-item>
          <el-form-item label="创建人员" prop="f_staff">
            <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <template #footer>
      <div class="drawer-footer">
        <el-button @click="drawerVisible = false">取消</el-button>
        <el-button v-show="!drawerProps.isView" type="primary" @click="handleSubmit">确定</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script setup lang="ts" name="SheepDrawer">
import ProTable from "@/components/ProTable/index.vue";
import { ref, reactive, computed } from "vue";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import { FeedingTypeType, ingredientsType, InventoryTypeType } from "@/assets/json/typeListJson";
import { G_slaughterG_salesTypeType, SellingType, VaccineTypeType } from "@/assets/json/typeListJson";
import UploadImg from "@/components/Upload/Img.vue";
import { validate_outNum } from "../api/manu";
import { ChatRound, CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";

import { ColumnProps, ProTableInstance } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { getManuList } from "../../inventoryDrug/api/manu";
import { Generate_outbound_no } from "../../feeding_out/api/manu";

const validateProps = (rule: any, value: any, callback: any) => {
  if (drawerProps.value.title === "编辑") callback();
  console.log(rule, value, callback);
  console.log(drawerProps.value.row.maker_id);
  validate_outNum({
    prop: rule.field,
    value: value,
    maker_id: drawerProps.value.row.maker_id,
    maker_name: drawerProps.value.row.maker_name,
    name: drawerProps.value.row.v_name,
    type: drawerProps.value.row.type
  }).then(res => {
    if (res.realcode === 200) {
      callback();
    } else if (res.realcode === 501) {
      ElMessageBox.alert(res.msg);
      callback();
    } else {
      if (res && res.hasOwnProperty("data")) {
        console.log(res.data);
        drawerProps.value.row.num = res.data;
      }
      ElMessageBox.alert(res.msg);
      callback();
      // callback(new Error(res.msg));
    }
  });
};
//   contact_phone: [{ required: true, message: "请输入联系电话" }],
const rules = reactive({
  maker_name: [{ required: true }],
  outbound_no: [{ required: true, message: "请输入出库单号" }],
  v_name: [{ required: true, message: "请输入农药信息" }],
  type: [{ required: true, message: "请选择类别" }],
  delivery_time: [{ required: true, message: "请选择出库时间" }],
  out_staff: [{ required: true, message: "请输入出库人员" }],
  num: [
    { required: true, message: "请输入出库数量" },
    { validator: validateProps, trigger: "blur" }
  ]
});

// 控制搜索框和表格的显示
const showSearch = ref(false);

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  // { prop: "operation", label: "操作", fixed: "left", width: 80 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "maker_name",
    label: "生产厂家",
    search: { el: "input" }
  },
  {
    prop: "type",
    label: "物资类型",
    enum: InventoryTypeType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  {
    prop: "goods",
    label: "农药信息",
    search: { el: "input" }
  },
  {
    prop: "ingredientsType",
    label: "成分类型",
    enum: ingredientsType
  },
  // {
  //   prop: "maker_id",
  //   label: "生产厂家id",
  //   search: { el: "input" }
  // },
  {
    prop: "quantity",
    label: "库存数量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "stockPrice",
    label: "库存价格"
  },
  {
    prop: "totalCost",
    label: "总花费"
  },
  {
    prop: "alert",
    label: "警戒数量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "f_date",
    label: "创建时间",
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  },
  // {
  //   prop: "operation",
  //   label: "操作",
  //   search: {
  //     el: "input",
  //     props: {
  //       type: "textarea"
  //     }
  //   }
  // },
  {
    prop: "f_staff",
    label: "创建人员",
    search: { el: "input" }
  },
  {
    prop: "out_time",
    label: "更新时间",
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  }
]);

const toggleSearchTable = () => {
  showSearch.value = !showSearch.value;
};

// 导出列表
const selectEwe = async selectedList => {
  console.log(selectedList);
  if (selectedList.length == 0) {
    ElMessage.warning("请选择要添加的草地记录");
    return;
  } else if (selectedList.length > 1) {
    ElMessageBox.confirm("只能选择1条记录?", "温馨提示", { type: "warning" });
    return;
  }
  // 获取选中记录的 ele_num 值

  const selectedVname = selectedList[0].goods;
  const selectedType = selectedList[0].type;
  const selectedMakername = selectedList[0].maker_name;
  const selectedingredientsType = selectedList[0].ingredientsType;
  // 确认提示
  try {
    await ElMessageBox.confirm(
      `确认选择厂家为 ${selectedMakername} 并且类型和名称为  ${selectedVname}
    的防护剂嘛?`,
      "温馨提示",
      {
        type: "warning"
      }
    );

    // 将选中的 想要的属性 值写入表单数据
    drawerProps.value.row.type = selectedType;
    drawerProps.value.row.v_name = selectedVname;
    drawerProps.value.row.maker_name = selectedMakername;
    drawerProps.value.row.ingredientsType = selectedingredientsType;
    showSearch.value = false;
    ElMessage.success("库存信息已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
};
// ProTable 实例引用
const proTable = ref<ProTableInstance>();
//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("getForage", getManuList(newParams));
  return getManuList(newParams);
};
// 动态调整宽度
const drawerWidth = computed(() => {
  return showSearch.value ? `${window.innerWidth}px` : "450px";
});

const handleInput = value => {
  // 将输入的值转换为整数
  drawerProps.value.row.num = parseInt(value, 10);
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

// 弹窗添加生产厂商
const openAddWindow = () => {
  let newWindow = window.open(
    "http://localhost:" + import.meta.env.VITE_PORT + "/#/supply/v_suppliersinfo/select_page",
    "name",
    "width=800,height=800,left=400,top=100"
  );
  window.onmessage = event => {
    if (event.origin === window.location.origin && event.data.hasOwnProperty("supplier_name")) {
      drawerProps.value.row.maker_name = event.data.supplier_name;
      drawerProps.value.row.maker_id = event.data.id;
      console.log(event);
    }
  };
};

// 接收父组件传过来的参数
const acceptParams = async (params: DrawerProps) => {
  showSearch.value = false;
  drawerProps.value = params;
  if (drawerProps.value.title === "新增") {
    console.log("自动生成单号");
    const generate_outbound_no = await Generate_outbound_no({ param: null, type: "疫苗" });
    console.log(generate_outbound_no);
    drawerProps.value.row.outbound_no = generate_outbound_no.data;
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

const Changedelivery_time = async value => {
  console.log("出库日期改变函数");
  console.log({ param: value });
  const generate_outbound_no = await Generate_outbound_no({ param: value, type: "疫苗" });
  console.log(generate_outbound_no);
  drawerProps.value.row.outbound_no = generate_outbound_no.data;
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
  padding-right: 30px;
}
.button1 {
  margin-top: 1px;
  margin-left: -40px;
}
.p1 {
  margin-left: 30px;
  font-size: 10px;
}
</style>
