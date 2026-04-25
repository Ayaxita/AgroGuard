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
          :model="drawerProps.row"
          label-width="120px"
          label-suffix=" :"
          :rules="rules"
          :disabled="drawerProps.isView"
          :hide-required-asterisk="drawerProps.isView"
        >
          <p style="color: red">注意！物资名称、物资类型、厂家信息，提交后不能修改</p>
          <el-button class="have" v-if="!ifBack" tag="div" role="button" tabindex="0" @click="clickAddinfoHave">
            我想要选择库存中已经存在的物品信息！
          </el-button>
          <el-button class="nohave" v-if="!ifBack" tag="div" role="button" tabindex="1" @click="clickAddinfonoHave">
            我想要增加当前库存中没有存在的物品信息！
          </el-button>
          <el-button v-if="ifBack && drawerProps.title === '新增'" tag="div" role="button" tabindex="2" @click="clickBackButton">
            返回上一页面
          </el-button>
          <el-form-item v-if="ifBack" label="类别" prop="type">
            <el-select v-model="drawerProps.row.type" clearable :disabled="drawerProps.title === '编辑' || ifHave === 1">
              <el-option v-for="item in VaccineTypeType" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <!-- 这一部分代码是想要做，自动补全下拉菜单的，由于时间问题没有成功实现这个目标，主要问题在于前端显示不正常，可以留下供之后选择使用
          <el-autocomplete
            v-model="drawerProps.row.v_name"
            :fetch-suggestions="querySearchAsync"
            placeholder="请输入农药信息"
            popper-append-to-body="false"
            @select="handleSelect"
          /> -->
          <el-form-item v-if="ifBack" label="防护剂名称" prop="v_name">
            <el-input
              v-model="drawerProps.row.v_name"
              clearable
              :disabled="drawerProps.title === '编辑' || ifHave === 1"
            ></el-input>
            <el-button
              v-if="ifHave === 1"
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
          <el-form-item v-if="ifBack" label="生产厂家" prop="maker_name">
            <el-input
              v-model.trim="drawerProps.row.maker_name"
              clearable
              :disabled="drawerProps.title === '编辑' || ifHave === 1"
            ></el-input>
            <el-button type="primary" plain @click="openAddWindow" v-if="drawerProps.title === '新增' && ifHave === -1">
              单机弹出添加框
            </el-button>
            <el-button
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
          <el-form-item v-if="ifBack" label="用途" prop="purpose">
            <el-input v-model="drawerProps.row.purpose" clearable></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="生产日期" prop="produce_date">
            <el-date-picker
              v-model="drawerProps.row.produce_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期"
              clearable
            />
          </el-form-item>
          <el-form-item v-if="ifBack" label="到期日期" prop="expiration_date">
            <el-date-picker
              v-model="drawerProps.row.expiration_date"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期"
              clearable
            />
          </el-form-item>
          <el-form-item v-if="ifBack" label="生产批号" prop="produce_num">
            <el-input v-model="drawerProps.row.produce_num" clearable></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="计量单位" prop="billing_unit">
            <el-input v-model="drawerProps.row.billing_unit" clearable></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="入库数量" prop="in_amount">
            <el-input type="number" v-model.number="drawerProps.row.in_amount" clearable @input="handleInput"></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="单价（元）" prop="unit_price">
            <el-input v-model.number="drawerProps.row.unit_price" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="总价（元）" prop="total_price">
            <el-input v-model.number="drawerProps.row.total_price" type="number" step="0.01" clearable disabled></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="运费（元）" prop="fare">
            <el-input v-model.number="drawerProps.row.fare" type="number" step="0.01" clearable></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="折合单价" prop="avg_price">
            <el-input v-model.number="drawerProps.row.avg_price" type="number" step="0.01" clearable disabled></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="入库时间" prop="in_time">
            <el-date-picker
              v-model="drawerProps.row.in_time"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="选择日期"
              clearable
            />
          </el-form-item>
          <!-- <el-form-item label="库存数量" prop="keep_amount">
            <el-input v-model="drawerProps.row.keep_amount" type="number" step="0.01" clearable></el-input>
          </el-form-item> -->
          <el-form-item v-if="ifBack" label="创建时间" prop="f_date">
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
          <el-form-item v-if="ifBack" label="创建人员" prop="f_staff">
            <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
          </el-form-item>
          <el-form-item v-if="ifBack" label="操作" prop="operation">
            <el-input v-model="drawerProps.row.operation" type="textarea" clearable></el-input>
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
import { ref, reactive, watch, watchEffect, computed } from "vue";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import { ingredientsType, VaccineTypeType } from "@/assets/json/typeListJson";
import ProTable from "@/components/ProTable/index.vue";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { InventoryTypeType, varietyType } from "@/assets/json/typeListJson";
import { getManuList } from "../../inventoryDrug/api/manu";
import { ChatRound, CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";

const rules = reactive({
  type: [{ required: true, message: "请选择类别" }],
  maker_name: [{ required: true, message: "请选择厂家" }],
  v_name: [{ required: true, message: "请输入农药信息" }],
  ingredientsType: [{ required: true, message: "请选择成分类别" }],
  produce_date: [{ required: true, message: "请选择生产日期" }],
  expiration_date: [{ required: true, message: "请选择到期日期" }],
  produce_num: [{ required: true, message: "请输入生产批号" }],
  in_amount: [{ required: true, message: "请输入入库数量" }],
  unit_price: [{ required: true, message: "请输入单价（元）" }],
  in_time: [{ required: true, message: "请选择入库时间" }]
});
// 控制搜索框和表格的显示
const showSearch = ref(false);
// 我准备在这里加一个控制切换表格内容的变量，主要目的是区别他想要增加现有的还是没有的防护剂/药物信息
// 0 : 代表 中立状态 1：代表 存在状态 -1：代表 不存在状态
const ifHave = ref(0);
// 我需要加一个点击事件的按钮
const clickAddinfoHave = () => {
  ifHave.value = 1;
  ifBack.value = true;
  drawerProps.value.row.type = null;
  drawerProps.value.row.v_name = null;
  drawerProps.value.row.maker_name = null;
  drawerProps.value.row.ingredientsType = null;
};
const clickAddinfonoHave = () => {
  ifHave.value = -1;
  ifBack.value = true;
  drawerProps.value.row.type = null;
  drawerProps.value.row.v_name = null;
  drawerProps.value.row.maker_name = null;
  drawerProps.value.row.ingredientsType = null;
};
const clickBackButton = () => {
  showSearch.value = false;
  ifHave.value = 0;
  ifBack.value = !ifBack.value;
  drawerProps.value.row.type = null;
  drawerProps.value.row.v_name = null;
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
  // 获取选中库存项

  const selectedGoods = selectedList[0].goods;
  const selectedType = selectedList[0].type;
  const selectedMakername = selectedList[0].maker_name;
  const selectedingredientsType = selectedList[0].ingredientsType;
  // 确认提示
  try {
    await ElMessageBox.confirm(
      `确认选择厂家为 ${selectedMakername} 并且类型和名称为  ${selectedGoods}
    的此项库存信息吗？`,
      "温馨提示",
      {
        type: "warning"
      }
    );

    // 将选中的 想要的属性 值写入表单数据
    drawerProps.value.row.type = selectedType;
    drawerProps.value.row.v_name = selectedGoods;
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
  console.log("getDrug", getManuList(newParams));
  return getManuList(newParams);
};
// 动态调整宽度
const drawerWidth = computed(() => {
  return showSearch.value ? `${window.innerWidth}px` : "450px";
});
const handleInput = value => {
  // 将输入的值转换为整数
  drawerProps.value.row.in_amount = parseInt(value, 10);
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

watchEffect(() => {
  if (drawerProps.value.title === "新增") {
    drawerProps.value.row.in_amount = 0;
    drawerProps.value.row.unit_price = 0;
    drawerProps.value.row.fare = 0;
  }
  if (drawerProps.value.title === "编辑" || drawerProps.value.title === "查看") {
    ifBack.value = true;
  }
});

watchEffect(() => {
  // console.log("in_amount", "计算了单价");
  drawerProps.value.row.total_price = drawerProps.value.row.in_amount * drawerProps.value.row.unit_price;
  drawerProps.value.row.avg_price =
    (drawerProps.value.row.total_price + parseFloat(drawerProps.value.row.fare)) / drawerProps.value.row.in_amount;
  // console.log(drawerProps.value.row.total_price, drawerProps.value.row.fare, drawerProps.value.row.in_amount);
});

// 弹窗添加生产厂商
const openAddWindow = () => {
  const host = window.location.host;
  const url = `http://${host}/#/supply/v_suppliersinfo/select_page`;
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
    if (!valid) {
      console.log("表单验证不通过，当前表单数据：", drawerProps.value.row);
      return;
    }
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

// 这一部分代码是想要做，自动补全下拉菜单的，由于时间问题没有成功实现这个目标，主要问题在于前端显示不正常，可以留下供之后选择使用
// const querySearchAsync = (queryString, cb) => {
//   // 发送请求到后端获取提示列表
//   const baseUrl = "http://localhost:5000";
//   fetch(`${baseUrl}/h_store/inventory/search?keyword=${queryString}`)
//     .then(response => {
//       if (!response.ok) {
//         throw new Error(`请求失败，状态码: ${response.status}`);
//       }
//       return response.json();
//     })
//     .then(data => {
//       if (data && data.constructor === Array) {
//         console.log(data);
//         cb(data);
//       } else {
//         console.error("后端返回的数据不是数组:", data);
//         cb([]);
//       }
//     })
//     .catch(error => {
//       console.error("请求出错:", error);
//       cb([]);
//     });
// };
// const handleSelect = item => {
//   console.log("选中的项:", item);
// };
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
