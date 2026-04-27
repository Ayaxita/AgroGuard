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
        <el-select v-model="selectedHouse" filterable placeholder="请先选择监测站点" style="width: 240px">
          <el-option v-for="item in houses" :key="item.value" :value="item.value" :label="item.label" />
        </el-select>
        <el-button type="primary" :icon="CirclePlus" @click="openDrawer('新增')">新增</el-button>
        <el-button type="danger" :icon="Delete" @click="deleteHurdleinfo(scope.selectedListIds)">删除</el-button>
        <el-button type="primary" :icon="CirclePlus" @click="setHouseHurdle(scope.selectedListIds)">合并监测站点</el-button>
        <el-button type="primary" :icon="ZoomOut" @click="unsealHouseHurdle(scope.selectedListIds)">拆分监测站点</el-button>
        <el-button type="primary" :icon="Refresh" plain @click="updateHurdle">清点数量</el-button>
        <el-button type="primary" :icon="MagicStick" plain @click="hurdleDisinfect(scope.selectedListIds)">防疫处理</el-button>
      </template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
      <!-- 表格操作 -->
      <template #operation="scope">
        <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button>
        <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)">编辑</el-button>
      </template>
    </ProTable>
    <GrassDrawer ref="drawerRef" />
    <ImportExcel ref="dialogRef" />
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive, onBeforeMount, h } from "vue";
import { useRouter } from "vue-router";
import { User } from "@/api/interface";
import { ElDatePicker, ElForm, ElFormItem, ElInput, ElMessage, ElMessageBox, ElOption, ElSelect } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import GrassDrawer from "../components/GrassDrawer.vue";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import {
  CircleCheck,
  CircleClose,
  CirclePlus,
  CirclePlusFilled,
  Delete,
  EditPen,
  MagicStick,
  Refresh,
  View,
  ZoomOut
} from "@element-plus/icons-vue";
import {
  getManuList,
  editManu,
  addManu,
  initHouse,
  delManu,
  updateHurdleNumber,
  disinfectHurdle,
  setHurdle,
  unsealHurdle
} from "../api/manu";
import { fieldDisinfectionMethodType, fieldFuntionType, fieldH_typeType, varietyType } from "@/assets/json/typeListJson";

const router = useRouter();

// ProTable 实例
const proTable = ref<ProTableInstance>();

const houses = ref<any>([]);
const selectedHouse = ref("");
// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
  return {
    list: data.list,
    total: data.total
  };
};
// 如果表格需要初始化请求参数，直接定义传给 ProTable (之后每次请求都会自动带上该参数，此参数更改之后也会一直带上，改变此参数会自动刷新表格数据)
const initParam = reactive({ house_id: selectedHouse });

//请求数据
// 如果你想在请求之前对当前请求参数做一些操作，可以自定义如下函数：params 为当前所有的请求参数（包括分页），最后返回请求列表接口
// 默认不做操作就直接在 ProTable 组件上绑定	:requestApi="getUserList"
const getTableList = (params: any) => {
  let newParams = JSON.parse(JSON.stringify(params));
  console.log("newParams", newParams);
  newParams.createTime && (newParams.startTime = newParams.createTime[0]);
  newParams.createTime && (newParams.endTime = newParams.createTime[1]);
  delete newParams.createTime;
  return getManuList(newParams);
};

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "id",
    label: "编号",
    search: {
      el: "input"
    }
  },
  {
    prop: "name",
    label: "监测地块名称",
    search: {
      el: "input"
    }
  },
  {
    prop: "function",
    label: "功能",
    enum: fieldFuntionType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "area",
    label: "面积(平方米)",
    search: {
      el: "input",
      props: { type: "number" }
    }
  },
  {
    prop: "h_type",
    label: "区域类型",
    enum: fieldH_typeType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "h_lwh",
    label: "区域尺寸",
    search: {
      el: "input"
    }
  },
  {
    prop: "sports_lwh",
    label: "生长区尺寸",
    search: {
      el: "input"
    }
  },
  {
    prop: "grass_type",
    label: "草地类型",
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "area_pro",
    label: "草地覆盖率",
    search: {
      el: "input"
    }
  },
  {
    prop: "grass_quantity",
    label: "地块数量",
    search: {
      el: "input",
      props: { type: "number" }
    }
  },
  {
    prop: "build_time",
    label: "建设时间",
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
    prop: "difinfect_time",
    label: "最后防疫时间",
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
    prop: "staff",
    label: "管理人员",
    search: {
      el: "input"
    }
  }
  // {
  //   prop: "f_staff",
  //   label: "创建人员",
  //   search: {
  //     el: "input"
  //   }
  // }
]);
// 初始化house

onBeforeMount(() => {
  initHouse().then((res: any) => {
    if (res.code === 200) {
      houses.value = res.data.list;
    } else {
      ElMessage.error("获取监测站点列表失败！");
    }
  });
});

//合并所选监测地块
const setHouseHurdle = async selectedListIds => {
  // 获取用户在表格中所选的监测地块
  const selectedGrassData = selectedListIds;

  if (!selectedGrassData || selectedGrassData.length === 0) {
    ElMessage.warning("请先选择要合并的监测地块！");
    return;
  }

  ElMessageBox.confirm(`确认将这${selectedGrassData.length}个监测地块合并为一个监测地块?`, "温馨提示", { type: "warning" }).then(
    () => {
      //通过这个函数把所选数据id传到后端
      setHurdle(selectedGrassData).then(res => {
        if (res.code === 200) {
          ElMessage.success("合并成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        } else {
          ElMessage.error("合并出错！");
        }
      });
    }
  );
};
//拆分所选监测地块
const unsealHouseHurdle = async selectedListIds => {
  // 获取用户在表格中所选的监测地块
  const selectedGrassData = selectedListIds;

  if (!selectedGrassData || selectedGrassData.length === 0) {
    ElMessage.warning("请先选择要拆分的监测地块！");
    return;
  }

  ElMessageBox.confirm(`确认将这${selectedGrassData.length}个监测地块拆分?`, "温馨提示", { type: "warning" }).then(() => {
    //通过这个函数把所选数据id传到后端
    unsealHurdle(selectedGrassData).then(res => {
      if (res.code === 200) {
        ElMessage.success("拆分成功！");
        proTable.value?.clearSelection();
        proTable.value?.getTableList();
      } else {
        ElMessage.error("拆分出错！");
      }
    });
  });
};
// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};
// 清点数量
const updateHurdle = async () => {
  ElMessageBox.confirm(
    "此操作会根据已有的草地数据，对所有监测地块的地块数量进行更新，并计算覆盖率，大概需要15秒，确认更新吗？",
    "温馨提示",
    {
      type: "warning"
    }
  ).then(() =>
    updateHurdleNumber().then(() => {
      ElMessage.success("更新成功！");
      proTable.value?.getTableList();
    })
  );
};
//删除
const deleteHurdleinfo = ids => {
  if (ids.length !== 0) {
    ElMessageBox.confirm(`确认删除监测地块?<br/>已选${ids.length}条记录`, "温馨提示", {
      type: "warning",
      dangerouslyUseHTMLString: true
    }).then(() => {
      delManu(ids).then(res => {
        if (res.code === 200) {
          ElMessage.success("删除成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要删除的监测站点！");
  }
};

const disinfect_info = ref<any>({
  date: null,
  staff: null,
  drug: null,
  dose: null,
  method: null,
  notes: null
});

//防疫处理
const hurdleDisinfect = async ids => {
  if (ids.length !== 0) {
    // console.log("好多条记录", grassinfo);
    ElMessageBox({
      title: "区域防疫处理",
      message: () => {
        return h("div", {}, [
          h(
            ElForm,
            {
              labelWidth: "150px",
              labelSuffix: " :",
              model: disinfect_info,
              rules: {
                date: [
                  {
                    required: true,
                    message: "请输入防疫日期"
                  }
                ],
                staff: [
                  {
                    required: true,
                    message: "请输入防疫人员"
                  }
                ],
                drug: [
                  {
                    required: true,
                    message: "请输入防疫药物"
                  }
                ],
                method: [
                  {
                    required: true,
                    message: "请选择防疫方法"
                  }
                ],
                notes: [
                  {
                    required: true,
                    message: "请输入备注"
                  }
                ]
              }
            },
            [
              h(
                ElFormItem,
                {
                  label: "防疫方法",
                  prop: "method"
                },
                [
                  h(
                    ElSelect,
                    {
                      modelValue: disinfect_info.value.method,
                      style: "width: 240px",
                      filterable: true,
                      placeholder: "请选择防疫方法",
                      "onUpdate:modelValue": val => {
                        disinfect_info.value.method = val;
                      }
                    },
                    fieldDisinfectionMethodType.map(item => {
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
                  label: "防疫药物",
                  prop: "drug"
                },
                [
                  h(ElInput, {
                    modelValue: disinfect_info.value.drug,
                    style: "width: 240px",
                    clearable: true,
                    placeholder: "请填写防疫药物",
                    "onUpdate:modelValue": val => {
                      disinfect_info.value.drug = val;
                      // console.log("newhurdle", new_hurdle.value, new_house.value);
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "稀释比例(重量/平米)",
                  prop: "dose"
                },
                [
                  h(ElInput, {
                    modelValue: disinfect_info.value.dose,
                    style: "width: 240px",
                    clearable: true,
                    placeholder: "请填写稀释比例",
                    "onUpdate:modelValue": val => {
                      disinfect_info.value.dose = val;
                      // console.log("newhurdle", new_hurdle.value, new_house.value);
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "防疫日期",
                  prop: "date"
                },
                [
                  h(ElDatePicker, {
                    modelValue: disinfect_info.value.date,
                    type: "date",
                    format: "YYYY-MM-DD",
                    valueFormat: "YYYY-MM-DD",
                    clearable: true,
                    placeholder: "请填写防疫日期",
                    "onUpdate:modelValue": val => {
                      disinfect_info.value.date = val;
                      // console.log("newhurdle", new_hurdle.value, new_house.value);
                    }
                  })
                ]
              ),
              h(
                ElFormItem,
                {
                  label: "防疫人员",
                  prop: "staff"
                },
                [
                  h(ElInput, {
                    modelValue: disinfect_info.value.staff,
                    style: "width: 240px",
                    clearable: true,
                    placeholder: "请填写防疫人员",
                    "onUpdate:modelValue": val => {
                      disinfect_info.value.staff = val;
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
                    modelValue: disinfect_info.value.notes,
                    style: "width: 240px",
                    type: "textarea",
                    placeholder: "请填写防疫药物",
                    "onUpdate:modelValue": val => {
                      disinfect_info.value.notes = val;
                      // console.log("newhurdle", new_hurdle.value, new_house.value);
                    }
                  })
                ]
              )
            ]
          ),
          h("p", `已选${ids.length}个监测地块`)
        ]);
      },
      showCancelButton: true
    }).then(() => {
      let params = {
        hurdle_ids: ids,
        ...disinfect_info.value
      };
      disinfect_info.value = {
        date: null,
        staff: null,
        drug: null,
        dose: null,
        method: null,
        notes: null
      };
      disinfectHurdle(params).then(res => {
        if (res.code === 200) {
          ElMessage.success("防疫处理成功！");
          // console.log("表的value", proTable.value);
          proTable.value?.getTableList();
        } else {
          ElMessage.error("区域防疫处理出错！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要防疫处理的监测地块！");
  }
};

// 打开 drawer(新增、查看、编辑)
// 由于后端逻辑，需要在编辑时不要house_id
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: title === "编辑" ? { ...row } : { ...row, ...initParam },
    api:
      title === "新增"
        ? addManu
        : title === "编辑"
          ? editManu
          : // : title === "合并"
            //   ? setHurdle
            //   : title === "拆分"
            //     ? unsealHurdle
            undefined,
    getTableList: proTable.value?.getTableList
  };
  console.log(params);
  drawerRef.value?.acceptParams(params);
};
</script>
