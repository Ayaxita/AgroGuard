<template>
  <div class="table-box">
    <ProTable
      ref="proTable"
      :columns="columns"
      :request-api="getTableList"
      :init-param="initParam"
      :data-callback="dataCallback"
      @drag-sort="sortTable"
      :search-col="4"
    >
      <!-- 表格 header 按钮 -->
      <template #tableHeader="scope">
        <el-button type="primary" size="small" :icon="CirclePlus" @click="openDrawer('新增')">新增记录</el-button>
        <el-button type="primary" size="small" :icon="Guide" plain @click="openTransfer(scope.selectedListIds)">
          记录转移
        </el-button>
        <el-button type="primary" size="small" :icon="PriceTag" plain @click="markSale(scope.selectedListIds)">
          标记售出
        </el-button>
        <el-button type="danger" size="small" :icon="CircleCloseFilled" plain @click="markDeath(scope.selectedListIds)">
          标记死亡
        </el-button>
        <el-button type="danger" size="small" :icon="CircleCloseFilled" plain @click="markDieOut(scope.selectedList)">
          标记淘汰
        </el-button>
        <el-button type="primary" size="small" :icon="Refresh" plain @click="updateMon_age">更新生长月数</el-button>
        <el-button type="primary" size="small" :icon="Refresh" plain @click="updateHouse">更新监测区域</el-button>
        <el-button type="primary" size="small" :icon="Grid" plain @click="generateQRCode(scope.selectedList)">
          生成二维码
        </el-button>
        <el-button type="primary" size="small" :icon="Collection" plain @click="toFamilyTree(scope.selectedListIds)">
          档案
        </el-button>
        <el-button type="primary" size="small" :icon="UploadFilled" plain @click="batchAddSheep"> 导入记录数据 </el-button>
        <el-button type="primary" size="small" :icon="Download" plain @click="downloadFile"> 导出记录数据 </el-button>
        <el-button
          type="primary"
          size="small"
          :icon="CirclePlus"
          plain
          @click="openimmunizationDrawer('新增免疫信息', scope.selectedList)"
        >
          批量加免疫信息
        </el-button>
        <el-button type="primary" size="small" :icon="Refresh" plain @click="updateGrand">更新关联信息</el-button>
      </template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
      <!-- usernameHeader -->
      <template #usernameHeader="scope">
        <el-button type="primary" @click="ElMessage.success('我是通过作用域插槽渲染的表头')">
          {{ scope.column.label }}
        </el-button>
      </template>
      <!-- createTime -->
      <template #createTime="scope">
        <el-button type="primary" link @click="ElMessage.success('我是通过作用域插槽渲染的内容')">
          {{ scope.row.createTime }}
        </el-button>
      </template>
      <!-- 表格操作 -->
      <template #operation="scope">
        <el-button type="primary" link :icon="View" @click="openDetail(scope.row)">查看</el-button>
        <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)" v-if="scope.row.state !== 2">
          编辑
        </el-button>
      </template>
    </ProTable>
    <SheepDrawer ref="drawerRef" />
    <immunizationDrawer ref="drawerRef2" />
    <ImportExcel ref="dialogRef" />
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive, onBeforeMount, h, computed } from "vue";
import { useRouter } from "vue-router";
import { User } from "@/api/interface";
import { useDownload } from "@/hooks/useDownload";
import { ElDatePicker, ElForm, ElFormItem, ElInput, ElMessage, ElMessageBox, ElOption, ElSelect } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import ImportExcel from "../components/ImportExcel/index.vue";
import SheepDrawer from "../components/SheepDrawer.vue";
import immunizationDrawer from "../components/immunizationDrawer.vue";
import { ProTableInstance, ColumnProps, HeaderRenderScope } from "@/components/ProTable/interface";
import {
  CirclePlus,
  Delete,
  EditPen,
  Download,
  Upload,
  View,
  Refresh,
  Collection,
  CircleCloseFilled,
  Grid,
  PriceTag,
  UploadFilled,
  Guide
} from "@element-plus/icons-vue";
import {
  addImmunization,
  getSheepList,
  editSheep,
  addSheep,
  exportSheepInfo,
  BatchAddSheep,
  markSheepDeath,
  updateMonAge,
  initHouseAndHurdle,
  sheepTransfer,
  updateHouseAndHurdle,
  markSheepDieOut,
  markSheepSale,
  BatchAddSheepTemp,
  initManu,
  updateGrandparents
} from "../api/sheep";
import {
  sexType,
  varietyType,
  colorType,
  gene_aType,
  gene_bType,
  gene_cType,
  stateType,
  purposeType,
  DeathCauseType,
  DeathHarmless_treatmentType,
  G_slaughterTypeType,
  SellingType,
  BooleanType
} from "@/assets/json/typeListJson";
import { placeholderSign } from "element-plus/es/components/table-v2/src/private";
import { commitUpdateDailyIncome } from "@/views/analysis/daily_income/api/manu";
import { commitUpdateAsset } from "@/views/analysis/sheep_asset/api/manu";

const router = useRouter();

const openDetail = params => {
  const href = router.resolve(`/basic/basicinfo/detail?ele_num=${params.ele_num}`);
  window.open(href.href, "_blank");
};
// ProTable 实例
const proTable = ref<ProTableInstance>();

const houses = ref<any>([]);
const manus = ref<any>([]);
// const selectedHouse = ref("");

/*陈皮:
 * 注意前端这边参数自带一个type
 * 现在已经删掉了，后端做查询的时候注意是否有type字段
 */
// 如果表格需要初始化请求参数，直接定义传给 ProTable (之后每次请求都会自动带上该参数，此参数更改之后也会一直带上，改变此参数会自动刷新表格数据)
// const initParam = reactive({ type: 1 });
const initParam = reactive({});

// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行

let datas;
const dataCallback = (data: any) => {
  datas = data;
  return {
    list: data.list,
    total: data.total
  };
};

//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  console.log("house", houses);
  console.log("value", houses.value);

  return getSheepList(newParams);
};

// 自定义渲染表头（使用tsx语法）
const headerRender = (scope: HeaderRenderScope<User.ResUserList>) => {
  return (
    <el-button type="primary" onClick={() => ElMessage.success("我是通过 tsx 语法渲染的表头")}>
      {scope.column.label}
    </el-button>
  );
};
// 存储选中的监测区域 ID
const selectedHouseId = ref<number | null>(null);
// **动态生成监测区域和监测地块**
const houseType = computed(() =>
  houses.value.map(house => ({
    label: house.house_name,
    value: house.house_name
  }))
);

const hurdleType = computed(() => {
  // if (!selectedHouseId.value) return [];
  // const house = houses.value.find(house => house.house_id === selectedHouseId.value);
  // return house
  //   ? house.hurdle_list.map(hurdle => ({
  //       label: hurdle.hurdle_name,
  //       value: hurdle.hurdle_id
  //     }))
  //   : [];
  if (!selectedHouseId.value) {
    // 如果未选择监测区域，显示所有监测地块
    return houses.value
      .flatMap(house => house.hurdle_list)
      .map(hurdle => ({
        label: hurdle.hurdle_name,
        value: hurdle.hurdle_name
      }));
  } else {
    // 如果已选择监测区域，只显示该监测区域的监测地块
    const selectedHouse = houses.value.find(house => house.house_name === selectedHouseId.value);
    return selectedHouse
      ? selectedHouse.hurdle_list.map(hurdle => ({
          label: hurdle.hurdle_name,
          value: hurdle.hurdle_name
        }))
      : [];
  }
});

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "ele_num",
    label: "草地编号",
    width: 150,
    search: { el: "input" }
  },
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
    enum: houseType,
    search: {
      el: "select",
      props: {
        onChange: val => {
          selectedHouseId.value = val;
          // 清空监测地块的搜索值并刷新表格
          if (proTable.value?.searchParam) {
            proTable.value.searchParam.hurdle_name = null;
            // proTable.value?.getTableList();
          }
        }
      }
    }
  },
  {
    prop: "hurdle_name",
    label: "监测地块",
    enum: hurdleType,
    search: {
      el: "select"
    }
  },
  {
    prop: "gene_a",
    label: "多批基因",
    enum: gene_aType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  // {
  //   prop: "gene_b",
  //   label: "抗病基因",
  //   enum: gene_bType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: { el: "select" }
  // },
  // {
  //   prop: "gene_c",
  //   label: "待定基因",
  //   enum: gene_cType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: { el: "select" }
  // },
  {
    prop: "f_staff",
    label: "添加人",
    width: 115,
    search: { el: "input", tooltip: "我是搜索提示" }
  },
  {
    prop: "f_date",
    label: "添加时间",
    width: 110,
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

onBeforeMount(() => {
  initHouseAndHurdle()
    .then(res => {
      if (res.code === 200) {
        houses.value = res.data.list;
        // 强制更新表格
        proTable.value?.getTableList();
        console.log("houses", houses.value);
      }
    })
    .catch(err => {
      ElMessage.error(`获取监测区域列表失败！ ${err}`);
    });
  initManu()
    .then(res => {
      if (res.code === 200) {
        manus.value = res.data.list;
        console.log("manus", manus.value);
      }
    })
    .catch(err => {
      ElMessage.error(`获取原产地列表失败！ ${err}`);
    });
});
// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

// 导出记录列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出记录数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportSheepInfo, "记录导出结果", proTable.value?.searchParam)
  );
};
const new_house = ref<any>(null);
const new_hurdle = ref<any>(null);

const new_model = computed(() => {
  return {
    house_id: new_house.value,
    hurdle_id: new_hurdle.value
  };
});
// 记录转移
const openTransfer = async sheepsinfo => {
  if (sheepsinfo.length !== 0) {
    if (sheepsinfo.some(item => datas.list.find(data => data.id === item).state === 2))
      return ElMessage.warning("不能选中已售出的记录！");
    //console.log("好多条记录", sheepsinfo);
    ElMessageBox({
      title: "记录转移",
      message: () => {
        return h("div", {}, [
          h(
            ElForm,
            {
              labelWidth: "100px",
              labelSuffix: " :",
              model: new_model,
              rules: {
                house_id: [{ required: true, message: "请选择新监测区域", trigger: "change" }],
                hurdle_id: [{ required: true, message: "请选择新监测地块", trigger: "change" }]
              }
            },
            [
              h(
                ElFormItem,
                {
                  label: "新监测区域",
                  prop: "house_id"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: new_house.value,
                      style: "width: 240px",
                      filterable: true,
                      placeholder: "请先选择监测区域",
                      "onUpdate:modelValue": val => {
                        new_house.value = val;
                        new_hurdle.value = null;
                      }
                    },
                    houses.value.map(item => {
                      return h(ElOption, {
                        label: item.house_name,
                        value: item.house_id
                      });
                    })
                  )
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "新监测地块",
                  prop: "hurdle_id"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: new_hurdle.value,
                      style: "width: 240px",
                      filterable: true,
                      placeholder: "请选择监测地块",
                      "onUpdate:modelValue": val => {
                        new_hurdle.value = val;
                        // console.log("newhurdle", new_hurdle.value, new_house.value);
                      }
                    },
                    houses.value
                      .find(item => item.house_id === new_house.value)
                      ?.hurdle_list.map(item => {
                        return h(ElOption, {
                          label: item.hurdle_name,
                          value: item.hurdle_id
                        });
                      })
                  )
                ]
              )
            ]
          ),
          h("p", `已选${sheepsinfo.length}条记录`)
        ]);
      },
      showCancelButton: true
    }).then(() => {
      let params = sheepsinfo.map(item => ({
        id: item,
        new_house_id: new_house.value,
        new_house_name: houses.value.find(item => item.house_id === new_house.value).house_name,
        new_hurdle_id: new_hurdle.value,
        new_hurdle_name: houses.value
          .find(item => item.house_id === new_house.value)
          .hurdle_list.find(item => item.hurdle_id === new_hurdle.value).hurdle_name
      }));
      new_house.value = null;
      new_hurdle.value = null;
      // console.log(params);
      sheepTransfer(params).then(res => {
        if (res.code === 200) {
          ElMessage.success("草地分区调整成功！");
          // console.log("表的value", proTable.value);
          proTable.value?.getTableList();
        } else {
          ElMessage.error("记录转移出错！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要转移的记录！");
  }
};

// 跳转记录档案详情页
//需要到authMenuList.json下面写路由
const toFamilyTree = sheepid => {
  // console.log(sheepid);
  if (sheepid.length === 1) {
    router.push(`/basic/basicinfo/useProTable/familyTree/${sheepid}?params=detail-page`);
  } else if (sheepid.length === 0) {
    ElMessage.warning("请先选择要查看的记录！");
  } else {
    ElMessage.warning("只能选择一条记录查看档案！");
  }
};

const saleProps = ref<any>({
  sales_date: null,
  sales_order: null,
  billing_unit: null,
  unit_price: null,
  weight: null,
  total_price: null,
  type: null,
  transportation: null,
  sales_site: null,
  name: null,
  buyer: null,
  buyer_phone: null,
  selling_type: null,
  quarantine_coding: null,
  age: null,
  medical_leave: null,
  notes: null
});
// 计算重量的函数
const calculateWeight = () => {
  const unitPrice = parseFloat(saleProps.value.unit_price);
  const totalPrice = parseFloat(saleProps.value.total_price);
  if (!isNaN(unitPrice) && !isNaN(totalPrice) && unitPrice !== 0) {
    saleProps.value.weight = (totalPrice / unitPrice).toFixed(2);
  }
};
// 标记售出
const markSale = async sheepsinfo => {
  if (sheepsinfo.length !== 0) {
    if (sheepsinfo.some(item => datas.list.find(data => data.id === item).state === 2))
      return ElMessage.warning("不能选中已售出的记录！");
    ElMessageBox({
      title: "标记售出",
      message: () => {
        return h("div", {}, [
          h(
            ElForm,
            {
              labelWidth: "120px",
              labelSuffix: " :",
              model: saleProps,
              rules: {
                sales_date: [{ required: true, message: "请填写销售日期" }],
                sales_order: [{ required: true, message: "请填写销售单号" }],
                type: [{ required: true, message: "请选择类型" }],
                ele_num: [{ required: true, message: "请填写草地编号" }],
                medical_leave: [{ required: true, message: "请选择是否执行安全间隔期" }],
                billing_unit: [{ required: true, message: "请填写计费单位" }],
                transportation: [{ required: true, message: "请填写运输方式" }],
                sales_site: [{ required: true, message: "请填写销售地点" }],
                name: [{ required: true, message: "请填写销往单位名称" }],
                buyer: [{ required: true, message: "请填写买方联系人" }],
                buyer_phone: [{ required: true, message: "请填写买方电话" }],
                selling_type: [{ required: true, message: "请选择销往对象类型" }]
                // notes: [{ required: true, message: "请填写备注信息" }]
              }
            },
            [
              h(
                ElFormItem,
                {
                  label: "销售日期",
                  prop: "sales_date"
                },
                [
                  h(ElDatePicker, {
                    modelValue: saleProps.value.sales_date,
                    type: "date",
                    format: "YYYY-MM-DD",
                    valueFormat: "YYYY-MM-DD",
                    clearable: true,
                    placeholder: "填写销售日期",
                    "onUpdate:modelValue": val => {
                      saleProps.value.sales_date = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "销售单号",
                  prop: "sales_order"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.sales_order,
                    style: "width: 240px",
                    placeholder: "请填写销售单号",
                    "onUpdate:modelValue": val => {
                      saleProps.value.sales_order = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "计费单位",
                  prop: "billing_unit"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.billing_unit,
                    style: "width: 240px",
                    filterable: true,
                    placeholder: "请填写计费单位",
                    "onUpdate:modelValue": val => {
                      saleProps.value.billing_unit = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "计费单价",
                  prop: "unit_price"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.unit_price,
                    type: "number",
                    step: 0.01,
                    placeholder: "请填写计费单价",
                    "onUpdate:modelValue": val => {
                      saleProps.value.unit_price = val;
                      calculateWeight();
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "总价",
                  prop: "total_price"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.total_price,
                    style: "width: 240px",
                    type: "number",
                    step: 0.01,
                    placeholder: "请填写总价",
                    "onUpdate:modelValue": val => {
                      saleProps.value.total_price = val;
                      calculateWeight();
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "类型",
                  prop: "type"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: saleProps.value.type,
                      style: "width: 240px",
                      filterable: true,
                      placeholder: "请填写类型",
                      "onUpdate:modelValue": val => {
                        saleProps.value.type = val;
                      }
                    },
                    G_slaughterTypeType.map(item => {
                      return h(ElOption, {
                        label: item.label,
                        value: item.value
                      });
                    })
                  )
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "运输方式",
                  prop: "transportation"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.transportation,
                    style: "width: 240px",
                    placeholder: "汽运：牌照号码",
                    "onUpdate:modelValue": val => {
                      saleProps.value.transportation = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "销售地点",
                  prop: "sales_site"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.sales_site,
                    style: "width: 240px",
                    placeholder: "请填写销售地点",
                    "onUpdate:modelValue": val => {
                      saleProps.value.sales_site = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "销售单位名称",
                  prop: "name"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.name,
                    style: "width: 240px",
                    placeholder: "请填写销售单位名称",
                    "onUpdate:modelValue": val => {
                      saleProps.value.name = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "买方联系人",
                  prop: "buyer"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.buyer,
                    style: "width: 240px",
                    placeholder: "请填写买方联系人",
                    "onUpdate:modelValue": val => {
                      saleProps.value.buyer = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "买方电话",
                  prop: "buyer_phone"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.buyer_phone,
                    style: "width: 240px",
                    placeholder: "请填写买方电话",
                    "onUpdate:modelValue": val => {
                      saleProps.value.buyer_phone = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "买方类型",
                  prop: "selling_type"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: saleProps.value.selling_type,
                      style: "width: 240px",
                      placeholder: "请填写买方类型",
                      "onUpdate:modelValue": val => {
                        saleProps.value.selling_type = val;
                      }
                    },
                    SellingType.map(item => {
                      return h(ElOption, {
                        label: item.label,
                        value: item.value
                      });
                    })
                  )
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "检测编码",
                  prop: "quarantine_coding"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.quarantine_coding,
                    style: "width: 240px",
                    placeholder: "请填写检测编码",
                    "onUpdate:modelValue": val => {
                      saleProps.value.quarantine_coding = val;
                    }
                  })
                ]
              ),
              // h(
              //   ElFormItem,
              //   {
              //     label: "记录年龄",
              //     prop: "age"
              //   },
              //   [
              //     h(ElInput, {
              //       modelValue: saleProps.value.age,
              //       style: "width: 240px",
              //       type: "number",
              //       step: 0.01,
              //       placeholder: "请填写记录年龄",
              //       "onUpdate:modelValue": val => {
              //         saleProps.value.age = val;
              //       }
              //     })
              //   ]
              // ),
              h(
                ElFormItem,
                {
                  label: "是否安全间隔期",
                  prop: "medical_leave"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: saleProps.value.medical_leave,
                      style: "width: 240px",
                      placeholder: "请选择是否安全间隔期",
                      "onUpdate:modelValue": val => {
                        saleProps.value.medical_leave = val;
                      }
                    },
                    BooleanType.map(item => {
                      return h(ElOption, {
                        label: item.label,
                        value: item.value
                      });
                    })
                  )
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "备注",
                  prop: "notes"
                },
                [
                  h(ElInput, {
                    modelValue: saleProps.value.notes,
                    style: "width: 240px",
                    type: "textarea",
                    placeholder: "请填写备注",
                    "onUpdate:modelValue": val => {
                      saleProps.value.notes = val;
                    }
                  })
                ]
              )
            ]
          ),
          h("p", `已选${sheepsinfo.length}条记录`)
        ]);
      },
      showCancelButton: true
    }).then(() => {
      let params = sheepsinfo.map(item => {
        return {
          ...saleProps.value,
          basic_id: item
        };
      });
      saleProps.value = {
        sales_date: null,
        sales_order: null,
        billing_unit: null,
        unit_price: null,
        weight: null,
        total_price: null,
        type: null,
        transportation: null,
        sales_site: null,
        name: null,
        buyer: null,
        buyer_phone: null,
        selling_type: null,
        quarantine_coding: null,
        age: null,
        medical_leave: null,
        notes: null
      };
      console.log(params);

      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0");
      const day = String(date.getDate()).padStart(2, "0");
      // 格式化为 YYYY-MM-DD
      const today = `${year}-${month}-${day}`;
      console.log(today);
      console.log(params[0].sales_date); //标记销售时的销售日期
      // if (params[0].sales_date < today) {
      //   console.log("我触发了");
      //   commitUpdateAsset(params);
      // }
      markSheepSale(params).then(res => {
        if (res.code === 200) {
          ElMessage.success("标记成功！");
          // 调用售出后的新函数（传递选中的记录ID）

          if (params[0].sales_date < today) {
            console.log("我触发了");
            commitUpdateAsset(params);
            commitUpdateDailyIncome(params); // 👈 这里新增调用,去更新这个销售日期的日收入报表
          }

          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        } else {
          ElMessage.error("标记失败！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要标记的记录！");
  }
};

const deathProps = ref<any>({
  basic_id: null,
  date: null,
  // 死亡生长月数要后端算
  // age: null,
  cause: null,
  harmless_treatment: null,
  t_time: null,
  t_staff: null,
  notes: null
});
// 标记死亡
const markDeath = async sheepsinfo => {
  if (sheepsinfo.length !== 0) {
    if (sheepsinfo.some(item => datas.list.find(data => data.id === item).state === 2))
      return ElMessage.warning("不能选中已售出的记录！");
    ElMessageBox({
      title: "标记死亡",
      message: () => {
        return h("div", {}, [
          h(
            ElForm,
            {
              labelWidth: "120px",
              labelSuffix: " :",
              model: deathProps,
              rules: {
                basic_id: [
                  {
                    required: true,
                    message: "请填写草地信息id",
                    trigger: "change"
                  }
                ],
                date: [
                  {
                    required: true,
                    message: "请填写死亡日期",
                    trigger: "change"
                  }
                ],
                cause: [
                  {
                    required: true,
                    message: "请填写死亡原因",
                    trigger: "change"
                  }
                ],
                harmless_treatment: [
                  {
                    required: true,
                    message: "请选择无害化处理方式",
                    trigger: "change"
                  }
                ],
                t_time: [
                  {
                    required: true,
                    message: "请填写处理时间",
                    trigger: "change"
                  }
                ],
                t_staff: [
                  {
                    required: true,
                    message: "请填写处理人",
                    trigger: "change"
                  }
                ],
                notes: [
                  {
                    required: true,
                    message: "请填写备注",
                    trigger: "change"
                  }
                ]
              }
            },
            [
              h(
                ElFormItem,
                {
                  label: "死亡日期",
                  prop: "date"
                },
                [
                  h(ElDatePicker, {
                    modelValue: deathProps.value.date,
                    type: "date",
                    format: "YYYY-MM-DD",
                    valueFormat: "YYYY-MM-DD",
                    clearable: true,
                    placeholder: "填写死亡日期",
                    "onUpdate:modelValue": val => {
                      deathProps.value.date = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "死亡原因",
                  prop: "cause"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: deathProps.value.cause,
                      style: "width: 240px",
                      filterable: true,
                      placeholder: "请填写死亡原因",
                      "onUpdate:modelValue": val => {
                        deathProps.value.cause = val;
                      }
                    },
                    DeathCauseType.map(item =>
                      h(ElOption, {
                        label: item.label,
                        value: item.value
                      })
                    )
                  )
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "无害化处理",
                  prop: "harmless_treatment"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: deathProps.value.harmless_treatment,
                      style: "width: 240px",
                      filterable: true,
                      placeholder: "请填写无害化处理原因",
                      "onUpdate:modelValue": val => {
                        deathProps.value.harmless_treatment = val;
                      }
                    },
                    DeathHarmless_treatmentType.map(item =>
                      h(ElOption, {
                        label: item.label,
                        value: item.value
                      })
                    )
                  )
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "处理时间",
                  prop: "t_time"
                },
                [
                  h(ElDatePicker, {
                    modelValue: deathProps.value.t_time,
                    type: "date",
                    format: "YYYY-MM-DD",
                    valueFormat: "YYYY-MM-DD",
                    clearable: true,
                    placeholder: "请填写处理时间",
                    "onUpdate:modelValue": val => {
                      deathProps.value.t_time = val;
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "处理人/单位",
                  prop: "t_staff"
                },
                [
                  h(ElInput, {
                    modelValue: deathProps.value.t_staff,
                    style: "width: 240px",
                    filterable: true,
                    placeholder: "请填写处理人/单位",
                    "onUpdate:modelValue": val => {
                      deathProps.value.t_staff = val;
                      // console.log("newhurdle", new_hurdle.value, new_house.value);
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "备注",
                  prop: "notes"
                },
                [
                  h(ElInput, {
                    modelValue: deathProps.value.notes,
                    style: "width: 240px",
                    filterable: true,
                    type: "textarea",
                    placeholder: "请填写备注",
                    "onUpdate:modelValue": val => {
                      deathProps.value.notes = val;
                    }
                  })
                ]
              )
            ]
          ),
          h("p", `已选${sheepsinfo.length}条记录`)
        ]);
      },
      showCancelButton: true
    }).then(() => {
      let params = sheepsinfo.map(item => {
        return {
          ...deathProps.value,
          basic_id: item
        };
      });
      deathProps.value = {
        basic_id: null,
        date: null,
        // 死亡生长月数要后端算
        // age: null,
        cause: null,
        harmless_treatment: null,
        t_time: null,
        t_staff: null,
        notes: null
      };
      markSheepDeath(params).then(res => {
        if (res.code === 200) {
          ElMessage.success("标记成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        } else {
          ElMessage.error("标记失败！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要标记的记录！");
  }
};

// 标记淘汰
const markDieOut = async sheepsinfo => {
  console.log("选中的淘汰信息", sheepsinfo);
  if (sheepsinfo.length !== 0) {
    if (sheepsinfo.some(item => item.state === 2)) return ElMessage.warning("不能选中已售出的记录！");
    sheepsinfo.forEach(item => {
      item.state = -1;
    });
    ElMessageBox.confirm(`确认标记淘汰?<br/>已选${sheepsinfo.length}条记录`, "温馨提示", {
      type: "warning",
      dangerouslyUseHTMLString: true
    }).then(() => {
      markSheepDieOut(sheepsinfo).then(res => {
        if (res === 200) {
          ElMessage.success("标记成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        } else {
          ElMessage.error("标记记录出错！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要标记的记录！");
  }
};

// 批量导入添加记录
const dialogRef = ref<InstanceType<typeof ImportExcel> | null>(null);
const batchAddSheep = () => {
  const params = {
    title: "记录",
    tempApi: BatchAddSheepTemp,
    importApi: BatchAddSheep,
    getTableList: proTable.value?.getTableList
  };
  dialogRef.value?.acceptParams(params);
};

// 生成二维码
const generateQRCode = async params => {
  if (params.length === 1) {
    const href = router.resolve(`/basic/basicinfo/qrcode?ele_num=${params[0].ele_num}`);
    console.log(href.href);
    window.open(href.href, "_blank");
  } else if (params.length === 0) {
    ElMessage.warning("请先选择要生成二维码的记录！");
  } else {
    ElMessage.warning("只能选择一条记录生成二维码！");
  }
};

// 更新生长月数
const updateMon_age = async () => {
  ElMessageBox.confirm(
    "此操作会根据当前日期更新所有记录生长月数，并对记录分类，耗时较多，请在空闲时操作，你确认要现在更新吗？",
    "温馨提示",
    { type: "warning" }
  ).then(() => {
    updateMonAge();
    window.location.reload();
  });
};

// 更新监测区域
const updateHouse = async () => {
  ElMessageBox.confirm(
    "此操作会根据已经上传的记录数据，对记录所在的监测区域进行更新，耗时较多，请在空闲时操作，你确认要现在更新吗？",
    "温馨提示",
    { type: "warning" }
  ).then(() =>
    updateHouseAndHurdle().then(() => {
      ElMessage.success("更新成功！");
    })
  );
};
// 更新关联信息
const updateGrand = async () => {
  ElMessageBox.confirm("此操作耗时较多，请在空闲时操作，你确认要现在更新吗？", "温馨提示", { type: "warning" }).then(() => {
    updateGrandparents();
    // window.location.reload();
  });
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof SheepDrawer> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    house_hurdle_list: houses.value,
    manu_list: manus.value,
    api: title === "新增" ? addSheep : title === "编辑" ? editSheep : undefined,
    getTableList: proTable.value?.getTableList
  };
  console.log(params);
  drawerRef.value?.acceptParams(params);
};
const drawerRef2 = ref<InstanceType<typeof immunizationDrawer> | null>(null);

const openimmunizationDrawer = (title: string, sheepList: Array<any>, row: Partial<User.ResUserList> = {}) => {
  //row: Partial<User.ResUserList> = {},
  if (sheepList.length !== 0) {
    if (sheepList.some(item => item.state === 2)) return ElMessage.warning("不能选中已售出的记录！");
    else {
      const params = {
        title,
        isView: title === "查看",
        row: { ...row },
        sheepList: sheepList,
        api: addImmunization,
        clearSelection: proTable.value?.clearSelection,
        getTableList: proTable.value?.getTableList
      };
      drawerRef2.value?.acceptParams(params);
    }
  } else {
    ElMessage.warning("请先选择要标记的记录！");
  }
};
</script>
