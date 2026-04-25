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
        <el-button type="primary" :icon="CirclePlus" @click="updateshocksheet">更新今日信息</el-button>
        <!-- <el-button type="primary" :icon="CirclePlus" @click="openDrawer('新增')">新增</el-button> -->
        <!-- <el-button type="danger" :icon="Delete" @click="deleteData(scope.selectedList)">删除</el-button> -->
        <el-button type="primary" :icon="Download" plain @click="downloadSelectFile(scope.selectedListIds)">
          导出所选数据
        </el-button>
        <el-button type="primary" :icon="Download" plain @click="downloadFile">导出所有数据</el-button>
      </template>
      <!-- Expand -->
      <template #expand="scope">
        {{ scope.row }}
      </template>
      <!-- 表格操作 scope -->
      <template #operation="">
        <!-- <el-button type="primary" link :icon="View" @click="openDrawer('查看', scope.row)">查看</el-button>
        <el-button type="primary" link :icon="EditPen" @click="openDrawer('编辑', scope.row)">编辑</el-button> -->
      </template>
    </ProTable>
    <GrassDrawer ref="drawerRef" />
  </div>
</template>

<script setup lang="tsx" name="useProTable">
import { ref, reactive, onMounted, watch, inject, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";
import { User } from "@/api/interface";
import { ElMessage, ElMessageBox } from "element-plus";
import ProTable from "@/components/ProTable/index.vue";
import GrassDrawer from "../components/GrassDrawer.vue";
import { ProTableInstance, ColumnProps, HeaderRenderScope } from "@/components/ProTable/interface";
import { CirclePlus, Delete, Download, EditPen, MessageBox, SetUp, View } from "@element-plus/icons-vue";
import { exportStockasset, getManuList, updatestocksheet } from "../api/manu";
import { colonyTransferReasonType, manuScaleType, manutypeType, sexType, DailyreportType } from "@/assets/json/typeListJson";
import { useDownload } from "@/hooks/useDownload";
import { useTable } from "@/hooks/useTable";
import { useTempStore } from "@/stores/modules/apiStore";

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
  // { prop: "operation", label: "操作", fixed: "left", width: 150 },
  /*{ type: "sort", label: "Sort", width: 80 },
  
  {
    prop: "basic_id",
    label: "草地基本信息",
    search: {
      el: "input"
    }
  },*/
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "date",
    label: "记录日期",
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
    prop: "forage",
    label: "草地投入",
    _children: [
      {
        prop: "garlicskin",
        label: "残渣类投入",
        _children: [
          {
            prop: "garlicskin_num",
            label: "数量"
          },
          {
            prop: "garlicskin_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "peanutseedling",
        label: "秸秆类投入",
        _children: [
          {
            prop: "peanutseedling_num",
            label: "数量"
          },
          {
            prop: "peanutseedling_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "ensilage",
        label: "青贮饲料",
        _children: [
          {
            prop: "ensilage_num",
            label: "数量"
          },
          {
            prop: "ensilage_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "otherforage",
        label: "其他投入",
        _children: [
          {
            prop: "otherforage_num",
            label: "数量"
          },
          {
            prop: "otherforage_val",
            label: "总价值"
          }
        ]
      }
    ]
  },
  {
    prop: "finefodder",
    label: "精准投入",
    _children: [
      {
        prop: "corn",
        label: "谷物类投入",
        _children: [
          {
            prop: "corn_num",
            label: "数量"
          },
          {
            prop: "corn_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "premix",
        label: "复合投入",
        _children: [
          {
            prop: "premix_num",
            label: "数量"
          },
          {
            prop: "premix_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "bran",
        label: "纤维类投入",
        _children: [
          {
            prop: "bran_num",
            label: "数量"
          },
          {
            prop: "bran_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "soybeanmeal",
        label: "豆类投入",
        _children: [
          {
            prop: "soybeanmeal_num",
            label: "数量"
          },
          {
            prop: "soybeanmeal_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "salt",
        label: "矿物质投入",
        _children: [
          {
            prop: "salt_num",
            label: "数量"
          },
          {
            prop: "salt_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "bakingsoda",
        label: "调节剂投入",
        _children: [
          {
            prop: "bakingsoda_num",
            label: "数量"
          },
          {
            prop: "bakingsoda_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "calciumlactate",
        label: "乳酸钙",
        _children: [
          {
            prop: "calciumlactate_num",
            label: "数量"
          },
          {
            prop: "calciumlactate_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "otherfinefodder",
        label: "其他精准投入",
        _children: [
          {
            prop: "otherfinefodder_num",
            label: "数量"
          },
          {
            prop: "otherfinefodder_val",
            label: "总价值"
          }
        ]
      }
    ]
  },
  {
    prop: "vaccine",
    label: "防护剂",
    _children: [
      {
        prop: "smallvaccine",
        label: "植保药剂",
        _children: [
          {
            prop: "smallvaccine_num",
            label: "数量"
          },
          {
            prop: "smallvaccine_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "threePfourD",
        label: "综合防护剂",
        _children: [
          {
            prop: "threePfourD_num",
            label: "数量"
          },
          {
            prop: "threePfourD_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "footAmouthdisease",
        label: "真菌病防护",
        _children: [
          {
            prop: "footAmouthdisease_num",
            label: "数量"
          },
          {
            prop: "footAmouthdisease_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "duolianbiying",
        label: "多联必应",
        _children: [
          {
            prop: "duolianbiying_num",
            label: "数量"
          },
          {
            prop: "duolianbiying_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "othervaccine",
        label: "其他防护剂",
        _children: [
          {
            prop: "othervaccine_num",
            label: "数量"
          },
          {
            prop: "othervaccine_val",
            label: "总价值"
          }
        ]
      }
    ]
  },
  {
    prop: "yaopin",
    label: "防护药品",
    _children: [
      {
        prop: "gentamicin",
        label: "庆大霉素",
        _children: [
          {
            prop: "gentamicin_num",
            label: "数量"
          },
          {
            prop: "gentamicin_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "zhongling",
        label: "中灵",
        _children: [
          {
            prop: "zhongling_num",
            label: "数量"
          },
          {
            prop: "zhongling_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "tilmicosin",
        label: "替米考星",
        _children: [
          {
            prop: "tilmicosin_num",
            label: "数量"
          },
          {
            prop: "tilmicosin_val",
            label: "总价值"
          }
        ]
      },
      {
        prop: "othermedicine",
        label: "其他防护药品",
        _children: [
          {
            prop: "othermedicine_num",
            label: "数量"
          },
          {
            prop: "othermedicine_val",
            label: "总价值"
          }
        ]
      }
    ]
  }
  // ,
  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

defineExpose({
  getTableList
});

//todo
//删除免疫信息
// const deleteData = async delinfo => {
//   console.log("选中的删除信息", delinfo);
//   if (delinfo.length !== 0) {
//     ElMessageBox.confirm(`确认删除对象?<br/>已选${delinfo.length}株`, "温馨提示", {
//       type: "warning",
//       dangerouslyUseHTMLString: true
//     }).then(() => {
//       delImmunizationinfo(delinfo).then(res => {
//         if (res === 200) {
//           ElMessage.success("删除成功！");
//           proTable.value?.clearSelection();
//           proTable.value?.getTableList();
//         } else {
//           ElMessage.error("删除免疫信息出错！");
//         }
//       });
//     });
//   } else {
//     ElMessage.warning("请先选择要标记的草地！");
//   }
// };
// 导出列表
const downloadFile = async () => {
  ElMessageBox.confirm("确认导出用户数据?", "温馨提示", { type: "warning" }).then(() =>
    useDownload(exportStockasset, "物料库存资产导出结果", proTable.value?.searchParam)
  );
};
//导出所选数据
const downloadSelectFile = async selectedListIds => {
  // 获取用户在表格中所选的草地记录数据
  const selectedGrassData = selectedListIds;

  if (!selectedGrassData || selectedGrassData.length === 0) {
    ElMessage.warning("请先选择要导出的草地记录数据！");
    return;
  }

  ElMessageBox.confirm(`确认导出所选的${selectedGrassData.length}条物料库存资产数据?`, "温馨提示", { type: "warning" }).then(
    () => {
      // 调用useDownload函数进行导出，并传入所选草地数据、导出文件名以及其他可能需要的参数（这里假设暂时不需要其他参数）
      useDownload(() => exportStockasset(selectedGrassData), `物料库存资产导出结果`, null);
    }
  );
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
// const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
//   const params = {
//     title,
//     isView: title === "查看",
//     row: { ...row },
//     api: title === "新增" ? addManu : title === "编辑" ? editManu : undefined,
//     getTableList: proTable.value?.getTableList
//   };
//   console.log(params);
//   drawerRef.value?.acceptParams(params);
// };
const updateshocksheet = () => {
  ElMessageBox.confirm(
    "此操作会根据当前日期更新物料库存信息，逻辑复杂，耗时较多（大约十五分钟），请在空闲时操作，你确认要现在更新吗？",
    "温馨提示",
    { type: "warning" }
  ).then(async () => {
    await updatestocksheet(); //isButtonDisabled.value = true;
    //computedTime();
  });
};
function computedTime() {
  new Date();
}
</script>
