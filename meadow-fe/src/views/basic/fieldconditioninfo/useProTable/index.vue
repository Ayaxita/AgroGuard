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
import { CirclePlus, Delete, EditPen, View } from "@element-plus/icons-vue";
import { getBreederConditionInfoList, editBreederConditionInfo, addBreederConditionInfo, delManu } from "../api/manu";
import {
  varietyType,
  colorType,
  fieldconditioninfo_MonageType,
  rankType,
  fieldconditioninfo_TestisShapeType,
  goodgrassAgetype
} from "@/assets/json/typeListJson";

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
  return getBreederConditionInfoList(newParams);
};

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  { prop: "operation", label: "操作", fixed: "left", width: 150 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  //还有一个mon_age字段，也叫"生长月数”
  /**附原后端注释
   *     ###1.5号新加字段
   *mon_age_choice=((0,'2生长月数'),(1,'6生长月数'),(2,'12生长月数'),(3,'24生长月数'),)
   */
  // mieosijfdosjdflasjdlkfjasdlkfjs
  {
    prop: "ele_num",
    label: "草地编号",
    width: 150,
    search: {
      el: "input"
    }
  },
  {
    prop: "variety",
    label: "草地类型",
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "date",
    label: "测量日期",
    width: 130,
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
    prop: "age",
    label: "生长月数"

    // enum: goodgrassAgetype,
    // fieldNames: { label: "label", value: "value" },
    // search: {
    //   el: "select"
    // }
  },
  // {
  //   prop: "color",
  //   label: "草地颜色",
  //   enum: colorType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: {
  //     el: "select"
  //   }
  // },
  {
    prop: "rank",
    label: "外貌等级",
    enum: rankType,
    fieldNames: { label: "label", value: "value" },
    search: {
      el: "select"
    }
  },
  {
    prop: "high",
    label: "体高",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "weight",
    label: "生物量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "Llong",
    label: "斜体长",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "bust",
    label: "胸围",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "back_fat",
    label: "茎径",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "eye",
    label: "叶面积",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "t_staff",
    label: "测量人员",
    search: {
      el: "input"
    }
  },
  {
    prop: "AE",
    label: "外貌评定",
    search: {
      el: "input",
      props: {
        type: "textarea"
      }
    }
  },
  {
    prop: "performance_traits",
    label: "生产性能",
    search: {
      el: "input"
    }
  },
  {
    prop: "with_births",
    label: "同批次数",
    search: {
      el: "input",
      props: {
        type: "number"
      }
    }
  },
  {
    prop: "wea_weight",
    label: "阶段生物量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "June_heavy",
    label: "六月生物量",
    search: {
      el: "input",
      props: {
        type: "number",
        step: 0.01
      }
    }
  },
  {
    prop: "health",
    label: "健康情况",
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
    prop: "notes",
    label: "备注",
    search: {
      el: "input",
      props: {
        type: "textarea"
      }
    }
  }
]);

// 表格拖拽排序
const sortTable = ({ newIndex, oldIndex }: { newIndex?: number; oldIndex?: number }) => {
  console.log(newIndex, oldIndex);
  console.log(proTable.value?.tableData);
  ElMessage.success("修改列表排序成功");
};

//删除
const deleteData = datasinfo => {
  if (datasinfo.length !== 0) {
    ElMessageBox.confirm(`确认删除?<br/>已选${datasinfo.length}项`, "温馨提示", {
      type: "warning",
      dangerouslyUseHTMLString: true
    }).then(() => {
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
    ElMessage.warning("请先选择要删除的记录！");
  }
};
// 打开 drawer(新增、查看、编辑)
const drawerRef = ref<InstanceType<typeof GrassDrawer> | null>(null);
const openDrawer = (title: string, row: Partial<User.ResUserList> = {}) => {
  const params = {
    title,
    isView: title === "查看",
    row: { ...row },
    api: title === "新增" ? addBreederConditionInfo : title === "编辑" ? editBreederConditionInfo : undefined,
    getTableList: proTable.value?.getTableList
  };
  console.log(params);
  drawerRef.value?.acceptParams(params);
};
</script>
