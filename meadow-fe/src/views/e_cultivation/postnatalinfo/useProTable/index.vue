<template>
  <div class="table-box">
    <ProTable
      ref="proTable"
      :columns="columns"
      :request-api="getTableList"
      :data-callback="dataCallback"
      @drag-sort="sortTable"
      :search-col="4"
    >
      <!-- 表格 header 按钮 -->
      <template #tableHeader="scope">
        <el-button type="primary" :icon="CirclePlus" @click="openDrawer('新增')">新增</el-button>
        <el-button type="danger" :icon="Delete" @click="deleteData(scope.selectedListIds)">删除</el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadSelectFile(scope.selectedListIds)">
          导出所选数据
        </el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadFile">导出所有数据</el-button>
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
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { User } from "@/api/interface";
import { ElMessage, ElMessageBox } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import GrassDrawer from "../components/GrassDrawer.vue";
import { ProTableInstance, ColumnProps } from "@/components/ProTable/interface";
import { CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import { getManuList, editManu, addManu, delManu, exportGrassInfo, getLamb } from "../api/manu";
import {
  colonyTransferReasonType,
  Ewe_conditionType,
  Ewe_healthType,
  Lamb_statType,
  manuScaleType,
  manutypeType
} from "@/assets/json/typeListJson";
import { useDownload } from "@/hooks/useDownload";

const router = useRouter();

// ProTable 实例
const proTable = ref<ProTableInstance>();

// dataCallback 是对于返回的表格数据做处理，如果你后台返回的数据不是 list && total 这些字段，可以在这里进行处理成这些字段
// 或者直接去 hooks/useTable.ts 文件中把字段改为你后端对应的就行
const dataCallback = (data: any) => {
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
  return getManuList(newParams);
};

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  // {
  //   prop: "breeding_id",
  //   label: "批次关联信息id",
  //   search: {
  //     el: "input"
  //   }
  // },
  {
    prop: "breeding_date",
    label: "批次建立日期",
    width: 115,
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
    prop: "delivery_date",
    label: "收割日期",
    width: 115,
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
  //   prop: "ram_id",
  //   label: "关联记录编号",
  //   search: {
  //     el: "input"
  //   }
  // },
  {
    prop: "ram_ele_num",
    label: "批次编号",
    width: 150,
    search: {
      el: "input"
    }
  },
  {
    prop: "ram_pre_num",
    label: "关联编号",
    width: 130,
    search: {
      el: "input"
    }
  },
  // {
  //   prop: "ewe_id",
  //   label: "关联记录编号",
  //   search: {
  //     el: "input"
  //   }
  // },
  {
    prop: "ewe_ele_num",
    label: "草地编号",
    width: 150,
    search: {
      el: "input"
    }
  },
  {
    prop: "ewe_pre_num",
    label: "地块编号",
    width: 130,
    search: {
      el: "input"
    }
  },

  {
    prop: "Booroola",
    label: "产量系数",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "ewe_health",
    label: "草地健康情况",
    enum: Ewe_healthType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "ewe_condition",
    label: "生长情况",
    enum: Ewe_conditionType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  // {
  //   prop: "lamb_ele_num",
  //   label: "批次编号",
  //   search: {
  //     el: "input"
  //   }
  // },
  // {
  //   prop: "lamb_state",
  //   label: "批次状态",
  //   enum: Lamb_statType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: {
  //     el: "select"
  //   }
  // },
  // {
  //   prop: "bir_weight",
  //   label: "出生生物量",
  //   search: {
  //     el: "input",
  //     props: {
  //       type: "number",
  //       step: 0.01
  //     }
  //   }
  // },
  {
    prop: "live_num",
    label: "批次数",
    search: {
      el: "input",
      props: {
        type: "number"
      }
    }
  },
  {
    prop: "birth_attendants",
    label: "采收人员",
    search: {
      el: "input"
    }
  },
  {
    prop: "f_staff",
    label: "创建人员",
    search: {
      el: "input"
    }
  },
  {
    prop: "f_date",
    label: "创建时间",
    width: 115,
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
    prop: "notes",
    label: "备注",
    search: {
      el: "input",
      props: {
        type: "textarea"
      }
    }
  },
  { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};
//todo
//删除
const deleteData = datasinfo => {
  if (datasinfo.length !== 0) {
    ElMessageBox.confirm(`确认删除信息?<br/>已选${datasinfo.length}条数据`, "温馨提示", {
      type: "warning",
      dangerouslyUseHTMLString: true
    }).then(() => {
      //通过这个函数把所选数据id传到后端
      delManu(datasinfo).then(res => {
        if (res.code === 200) {
          ElMessage.success("删除成功！");
          proTable.value?.clearSelection();
          proTable.value?.getTableList();
        } else {
          ElMessage.error("删除出错！");
        }
      });
    });
  } else {
    ElMessage.warning("请先选择要删除的信息！");
  }
};
// const deleteData = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
//   console.log(newIndex, oldIndex);
//   console.log(proTable.value?.tableData);
//   ElMessage.success("修改列表排序成功");
// };
// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportGrassInfo, "收割后信息导出结果", proTable.value?.searchParam)
  );
};
//导出所选数据
const downloadSelectFile = async selectedListIds => {
  // 获取用户在表格中所选的记录数据
  const selectedGrassData = selectedListIds;

  if (!selectedGrassData || selectedGrassData.length === 0) {
    ElMessage.warning("请先选择要导出的数据！");
    return;
  }

  ElMessageBox.confirm(`确认导出所选的${selectedGrassData.length}条数据?`, "温馨提示", { type: "warning" }).then(() => {
    // 调用useDownload函数进行导出，并传入所选记录数据、导出文件名以及其他可能需要的参数（这里假设暂时不需要其他参数）
    useDownload(() => exportGrassInfo(selectedGrassData), `收割后信息导出结果`, null);
  });
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
const openDrawer = async (title: string, row: Partial<User.ResUserList> = {}) => {
  // 动态检查是否包含 ewe_id等信息
  const eweId = "ewe_id" in row ? row.ewe_id : undefined;
  const ramId = "ram_id" in row ? row.ram_id : undefined;
  const deliveryDate = "delivery_date" in row ? row.delivery_date : undefined;

  console.log(eweId);
  console.log(ramId);

  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    api: title === "新增" ? addManu : title === "编辑" ? editManu : undefined,
    getTableList: proTable.value?.getTableList
  };

  console.log("传入参数:", params);

  // 如果是查看或编辑，调用后端接口获取更多信息
  if (title === "查看" || title === "编辑") {
    if (eweId && ramId && deliveryDate) {
      const combinedParams = { ewe_id: eweId, ram_id: ramId, delivery_date: deliveryDate };
      console.log(combinedParams);

      try {
        const resp = await getLamb(combinedParams);
        console.log("获取到的关联记录信息:", resp);

        // 强制断言 resp.data 为包含 list 字段的对象
        const data = resp.data as { list: any[] };

        // 如果 list 存在且不为空
        if (data.list && data.list.length > 0) {
          // const firstItem = data.list[0]; // 假设你需要的是 list 的第一项
          // params.row = { ...params.row, ...firstItem }; // 将数据合并
          // 如果 list 存在且不为空
          // 动态将所有返回的 list 添加到 row 中
          data.list.forEach((listItem, index) => {
            // 创建字段名，例如 list_0, list_1 等
            const listKey = `list_${index + 1}`;
            params.row = { ...params.row, [listKey]: listItem };
          });
          console.log("更新后的参数:", params);
        } else {
          console.warn("返回的数据列表为空");
        }
      } catch (err) {
        console.error("获取关联记录信息失败:", err);
      }
    } else {
      console.warn("缺少必要字段: ewe_id 或 ram_id");
    }
  }

  drawerRef.value?.acceptParams(params);
};
</script>
