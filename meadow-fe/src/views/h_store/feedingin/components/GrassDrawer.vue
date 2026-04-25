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
          <!-- 类型 -->
          <p class="p1" style="color: red">注意！物资名称、物资类型、厂家信息，提交后不能修改</p>
          <el-button class="have" v-if="!ifBack" tag="div" role="button" tabindex="0" @click="clickAddinfoHave">
            我想要选择库存中已经存在的物品信息！
          </el-button>
          <el-button class="nohave" v-if="!ifBack" tag="div" role="button" tabindex="1" @click="clickAddinfonoHave">
            我想要增加当前库存中没有存在的物品信息！
          </el-button>
          <el-button v-if="ifBack && drawerProps.title === '新增'" tag="div" role="button" tabindex="2" @click="clickBackButton">
            返回上一页面
          </el-button>
          <!-- 类型 -->
          <el-form-item v-if="ifBack" label="类型" prop="type">
            <el-select v-model="drawerProps.row.type" clearable :disabled="drawerProps.title === '编辑' || ifHave === 1">
              <el-option v-for="item in FeedingTypeType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>

          <!-- 草地投入名称 -->
          <el-form-item v-if="ifBack" label="草地投入名称" prop="f_name">
            <el-input
              v-model="drawerProps.row.f_name"
              clearable
              :disabled="drawerProps.title === '编辑' || ifHave === 1"
            ></el-input>
            <!-- 选择物料的按钮 -->
            <el-button
              v-if="ifHave === 1"
              size="small"
              type="primary"
              class="ml-2"
              @click="toggleSearchTable"
              :disabled="drawerProps.title === '编辑'"
            >
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              选择已有草地投入信息
            </el-button>
          </el-form-item>
          <!-- 生产厂家 -->
          <el-form-item v-if="ifBack" label="生产厂家" prop="maker_name">
            <el-input
              v-model.trim="drawerProps.row.maker_name"
              clearable
              :disabled="drawerProps.title === '编辑' || ifHave === 1"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button
              class="button1"
              type="primary"
              plain
              @click="openAddWindow"
              v-if="drawerProps.title === '新增' && ifHave === -1"
            >
              单机弹出添加框
            </el-button>
            <el-button
              class="button2"
              type="primary"
              plain
              @click="drawerProps.row.maker_name = null"
              v-if="drawerProps.title === '新增' && ifHave === -1"
            >
              取消选择
            </el-button>
          </el-form-item>
          <el-form-item v-if="ifBack" label="成分类型" prop="ingredientsType">
            <el-select
              v-model="drawerProps.row.ingredientsType"
              clearable
              :disabled="drawerProps.title === '编辑' || ifHave === 1"
            >
              <el-option v-for="item in ingredientsType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <!-- 仓库 -->
          <el-form-item v-if="ifBack" label="仓库" prop="warehouse_num">
            <el-input type="number" v-model="drawerProps.row.warehouse_num" clearable></el-input>
          </el-form-item>

          <!-- 营养成分 -->
          <el-form-item v-if="ifBack" label="营养成分" prop="nutrients">
            <el-input v-model="drawerProps.row.nutrients" type="textarea" clearable></el-input>
          </el-form-item>

          <!-- 购买时间 -->
          <el-form-item v-if="ifBack" label="购买时间" prop="buy_time">
            <el-date-picker
              v-model="drawerProps.row.buy_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期"
              clearable
            />
          </el-form-item>

          <!-- 计费单位 -->
          <el-form-item v-if="ifBack" label="计费单位" prop="billing_unit">
            <el-input v-model="drawerProps.row.billing_unit" clearable></el-input>
          </el-form-item>

          <!-- 重量 -->
          <el-form-item v-if="ifBack" label="重量" prop="quantity">
            <el-input v-model.number="drawerProps.row.quantity" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 单价（元） -->
          <el-form-item v-if="ifBack" label="单价（元）" prop="unit_price">
            <el-input v-model.number="drawerProps.row.unit_price" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 总价（元） -->
          <el-form-item v-if="ifBack" label="总价（元）" prop="total_price">
            <el-input v-model.number="drawerProps.row.total_price" type="number" step="0.01" clearable disabled></el-input>
          </el-form-item>

          <!-- 运费（元） -->
          <el-form-item v-if="ifBack" label="运费（元）" prop="fare">
            <el-input v-model.number="drawerProps.row.fare" type="number" step="0.01" clearable></el-input>
          </el-form-item>

          <!-- 折合单价 -->
          <el-form-item v-if="ifBack" label="折合单价" prop="avg_price">
            <el-input v-model.number="drawerProps.row.avg_price" type="number" step="0.01" clearable disabled></el-input>
          </el-form-item>

          <!-- 规格 -->
          <el-form-item v-if="ifBack" label="规格" prop="specifications">
            <el-input v-model="drawerProps.row.specifications" clearable></el-input>
          </el-form-item>

          <!-- 用途 -->
          <el-form-item v-if="ifBack" label="用途" prop="purpose">
            <el-input v-model="drawerProps.row.purpose" type="textarea" clearable></el-input>
          </el-form-item>

          <!-- 原材料含水量 -->
          <el-form-item v-if="ifBack" label="原材料含水量" prop="water_content">
            <el-input v-model="drawerProps.row.water_content" clearable></el-input>
          </el-form-item>

          <!-- 原材料霉变 -->
          <el-form-item v-if="ifBack" label="原材料霉变" prop="mildew">
            <el-input v-model="drawerProps.row.mildew" clearable></el-input>
          </el-form-item>

          <!-- 原材料杂质含量 -->
          <el-form-item v-if="ifBack" label="原材料杂质含量" prop="impurity_content">
            <el-input v-model="drawerProps.row.impurity_content" clearable></el-input>
          </el-form-item>

          <!-- 备注信息 -->
          <el-form-item v-if="ifBack" label="备注信息" prop="notes">
            <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
          </el-form-item>

          <!-- 库存数量 -->
          <!-- <el-form-item label="库存数量" prop="keep_amount">
          <el-input v-model="drawerProps.row.keep_amount" type="number" step="0.01" clearable></el-input>
        </el-form-item> -->

          <!-- 创建时间 -->
          <el-form-item v-if="ifBack" label="创建时间" prop="f_date">
            <el-date-picker
              v-model="drawerProps.row.f_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              :placeholder="`${new Date().getFullYear()}-${new Date().getMonth() + 1}-${new Date().getDate()}`"
              disabled
              clearable
            />
          </el-form-item>

          <!-- 创建人员 -->
          <el-form-item v-if="ifBack" label="创建人员" prop="f_staff">
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

<script setup lang="ts" name="GrassDrawer">
import { ref, reactive, watchEffect, computed } from "vue";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import {
  BooleanType,
  FeedingTypeType,
  G_slaughterTypeType,
  ingredientsType,
  InventoryTypeType,
  SellingType
} from "@/assets/json/typeListJson";
import { ColumnProps, ProTableInstance } from "@/components/ProTable/interface";
import { getManuList } from "../../inventoryForage/api/manu";
import { ChatRound, CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import { User } from "@/api/interface";

const rules = reactive({
  maker_name: [{ required: true }],
  type: [{ required: true, message: "请选择类型" }],
  f_name: [{ required: true, message: "请填写草地投入名称" }],
  ingredientsType: [{ required: true, message: "请选择成分类别" }],
  // nutrients: [{ required: true, message: "请填写营养成分" }],
  buy_time: [{ required: true, message: "请选择购买时间" }],
  billing_unit: [{ required: true, message: "请填写计费单位" }],
  quantity: [{ required: true, message: "请填写重量" }],
  unit_price: [{ required: true, message: "请填写单价（元）" }]
  // specifications: [{ required: true, message: "请填写规格" }],
  // water_content: [{ required: true, message: "请填写原材料含水量" }],
  // mildew: [{ required: true, message: "请填写原材料霉变情况" }],
  // impurity_content: [{ required: true, message: "请填写原材料杂质含量" }],
  // notes: [{ required: true, message: "请填写备注信息" }]
});
// 控制搜索框和表格的显示
const showSearch = ref(false);
// 我准备在这里加一个控制切换表格内容的变量，主要目的是区别他想要增加现有的还是没有的草地投入信息
// 0 : 代表 中立状态 1：代表 存在状态 -1：代表 不存在状态
const ifHave = ref(0);
// 我需要加一个点击事件的按钮
const clickAddinfoHave = () => {
  ifHave.value = 1;
  ifBack.value = true;
  drawerProps.value.row.type = null;
  drawerProps.value.row.f_name = null;
  drawerProps.value.row.maker_name = null;
  drawerProps.value.row.ingredientsType = null;
};
const clickAddinfonoHave = () => {
  ifHave.value = -1;
  ifBack.value = true;
  drawerProps.value.row.type = null;
  drawerProps.value.row.f_name = null;
  drawerProps.value.row.maker_name = null;
  drawerProps.value.row.ingredientsType = null;
};
const clickBackButton = () => {
  showSearch.value = false;
  ifHave.value = 0;
  ifBack.value = !ifBack.value;
  drawerProps.value.row.type = null;
  drawerProps.value.row.f_name = null;
  drawerProps.value.row.maker_name = null;
  drawerProps.value.row.ingredientsType = null;
};
// 如果这样的话我还需要控制返回按键的状态
// false 表示在第一层 true表示在第二层
const ifBack = ref(false);
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
    prop: "stockPrice",
    label: "库存价格"
  },
  {
    prop: "totalCost",
    label: "总花费"
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
  // 获取选中库存项

  const selectedGoods = selectedList[0].goods;
  const selectedType = selectedList[0].type;
  const selectedMakername = selectedList[0].maker_name;
  const selectedingredientsType = selectedList[0].ingredientsType;
  // 确认提示
  try {
    await ElMessageBox.confirm(
      `确认选择厂家为 ${selectedMakername} 并且类型和名称为  ${selectedGoods}
    的草地投入信息吗？`,
      "温馨提示",
      {
        type: "warning"
      }
    );

    // 将选中的 想要的属性 值写入表单数据
    drawerProps.value.row.type = selectedType;
    drawerProps.value.row.f_name = selectedGoods;
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

watchEffect(() => {
  if (drawerProps.value.title === "新增") {
    drawerProps.value.row.quantity = 0;
    drawerProps.value.row.unit_price = 0;
    drawerProps.value.row.fare = 0;
  }
  if (drawerProps.value.title === "编辑" || drawerProps.value.title === "查看") {
    ifBack.value = true;
  }
});

watchEffect(() => {
  // console.log("in_amount", "计算了单价");
  drawerProps.value.row.total_price = drawerProps.value.row.quantity * drawerProps.value.row.unit_price;
  drawerProps.value.row.avg_price =
    (drawerProps.value.row.total_price + parseFloat(drawerProps.value.row.fare)) / drawerProps.value.row.quantity;
  // console.log(drawerProps.value.row.total_price, drawerProps.value.row.fare, drawerProps.value.row.in_amount);
});
// 弹窗添加生产厂商
const openAddWindow = () => {
  // 获取当前父页面的主机名和端口号
  const host = window.location.host;
  const url = `http://${host}/#/supply/f_suppliersinfo/select_page`;
  let newWindow = window.open(url, "name", "width=800,height=800,left=400,top=100");
  window.onmessage = event => {
    if (event.origin === window.location.origin && event.data.hasOwnProperty("supplier_name")) {
      drawerProps.value.row.maker_name = event.data.supplier_name;
      drawerProps.value.row.maker_id = event.data.id;
      console.log(event);
    }
  };
};

// 接收父组件传过来的参数
const acceptParams = (params: DrawerProps) => {
  ifHave.value = 0;
  ifBack.value = false;
  showSearch.value = false;
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
.have {
  width: 80%;
  height: 200px;
  margin-left: 10%;
}
.nohave {
  width: 80%;
  height: 200px;
  margin-top: 50px;
  margin-left: 10%;
}
</style>
