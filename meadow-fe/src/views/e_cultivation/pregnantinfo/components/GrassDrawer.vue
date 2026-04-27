<template>
  <el-drawer v-model="drawerVisible" :destroy-on-close="true" :size="drawerWidth" :title="`${drawerProps.title}`">
    <div class="drawer-container">
      <!-- 左侧：搜索框和表格 -->
      <div class="left-section" v-if="showSearch">
        <!-- 搜索框 -->
        <!-- <el-form :model="searchParams" class="search-form">
                <el-form-item label="搜索条件" prop="search">
                  <el-input v-model="searchParams.search" clearable placeholder="请输入搜索条件" />
                </el-form-item>
                <el-button type="primary" @click="handleSearch">搜索</el-button>
              </el-form> -->

        <!-- ProTable -->
        <ProTable ref="proTable" :columns="columns" :request-api="getTableList" :data-callback="dataCallback" :search-col="4">
          <!-- 表格 header 按钮 -->
          <template #tableHeader="scope">
            <el-button type="primary" :icon="CirclePlus" @click="selectGrass(scope.selectedList)">选择</el-button>
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
          <el-form-item label="草地编号" prop="ewe_ele_num">
            <el-button @click="toggleSearchTable" size="small" type="primary" class="ml-2">
              <!-- {{ showSearch ? "隐藏搜索" : "显示搜索" }} -->
              添加关联信息
            </el-button>
            <el-input v-model="drawerProps.row.ewe_ele_num" clearable></el-input>
          </el-form-item>
          <el-form-item label="地块编号" prop="ewe_pre_num">
            <el-input v-model="drawerProps.row.ewe_pre_num" clearable></el-input>
          </el-form-item>
          <el-form-item label="检查类别" prop="check_type">
            <el-input v-model="drawerProps.row.check_type" clearable></el-input>
          </el-form-item>
          <!-- <el-form-item label="培育信息id" prop="breeding_id">
        <el-input type="number" v-model="drawerProps.row.breeding_id" clearable></el-input>
      </el-form-item> -->

          <el-form-item label="孕检信息" prop="In_pregnancy">
            <el-input v-model="drawerProps.row.In_pregnancy" clearable></el-input>
          </el-form-item>
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
          <el-form-item label="创建人员" prop="f_staff">
            <el-input v-model="drawerProps.row.f_staff" clearable></el-input>
          </el-form-item>
          <el-form-item label="备注" prop="notes">
            <el-input v-model="drawerProps.row.notes" type="textarea" clearable></el-input>
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
import { ref, reactive, computed } from "vue";
import { ElMessage, ElMessageBox, FormInstance } from "element-plus";
import { CirclePlus, Delete, Download, EditPen, View } from "@element-plus/icons-vue";
import ProTable from "@/components/ProTable/index.vue";
import { getManuList } from "../../breedinginfo/api/manu";
import { ColumnProps } from "@/components/ProTable/interface";
import { User } from "@/api/interface";
import { Breeding_stateType, Breeding_wayType, varietyType } from "@/assets/json/typeListJson";

const rules = reactive({
  check_type: [{ required: true, message: "请填写检查类别" }],
  // breeding_id: [{ required: true, message: "请填写培育信息id" }],
  In_pregnancy: [{ required: true, message: "请填写孕检信息" }]
  // notes: [{ required: true, message: "请填写备注" }]
});

// 表格配置项
const columns = reactive<ColumnProps<User.ResUserList>[]>([
  { type: "selection", fixed: "left", width: 70 },
  // { type: "sort", label: "Sort", width: 80 },
  // { type: "expand", label: "Expand", width: 85 },
  {
    prop: "ewe_ele_num",
    label: "草地编号",
    width: 150,
    search: {
      el: "input"
      // props: {
      //   type: "number"
      // }
    }
  },
  {
    prop: "ewe_pre_num",
    label: "地块编号",
    width: 150,
    search: {
      el: "input"
      // props: {
      //   type: "number"
      // }
    }
  },

  {
    prop: "ewe_variety",
    label: "关联草地类型",
    enum: varietyType,
    fieldNames: { label: "label", value: "value" },
    search: { el: "select" }
  },
  // {
  //   prop: "ram_ele_num",
  //   label: "草地编号",
  //   search: {
  //     el: "input"
  //     // props: {
  //     //   type: "number"
  //     // }
  //   }
  // },
  // {
  //   prop: "ram_pre_num",
  //   label: "地块编号",
  //   search: {
  //     el: "input"
  //     // props: {
  //     //   type: "number"
  //     // }
  //   }
  // },
  // {
  //   prop: "ram_variety",
  //   label: "关联草地类型",
  //   enum: varietyType,
  //   fieldNames: { label: "label", value: "value" },
  //   search: { el: "select" }
  // },
  {
    prop: "breeding_date",
    label: "批次建立日期",
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
    prop: "pre_production_date",
    label: "预产日期",
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
    prop: "staff",
    label: "操作师",
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
    width: 130,
    search: {
      el: "date-picker",
      props: {
        type: "daterange",
        format: "YYYY-MM-DD",
        "value-format": "YYYY-MM-DD"
      }
    }
  }
  // { prop: "operation", label: "操作", fixed: "right", width: 150 }
]);
// 控制搜索框和表格的显示
const showSearch = ref(false);
// 切换显示搜索框和表格,并搜索符合条件的关联记录信息
const toggleSearchTable = () => {
  showSearch.value = !showSearch.value;
};
// 动态调整宽度
const drawerWidth = computed(() => {
  return showSearch.value ? `${window.innerWidth}px` : "450px";
});
//选择记录
const selectGrass = async selectedList => {
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
    await ElMessageBox.confirm(`确认选择草地编号为 ${selectedItem.ewe_ele_num} 的记录?`, "温馨提示", {
      type: "warning"
    });

    // 将选中的 ele_num 值写入表单数据
    drawerProps.value.row.ewe_ele_num = selectedItem.ewe_ele_num;
    drawerProps.value.row.ewe_pre_num = selectedItem.ewe_pre_num;
    drawerProps.value.row.breeding_id = selectedItem.id;

    // 关闭选择表格
    showSearch.value = false;

    ElMessage.success("编号已成功添加");
  } catch (error) {
    console.log("操作取消");
  }
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
  console.log("getManuList", getManuList(newParams));
  return getManuList(newParams);
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
  drawerProps.value = params;
  drawerVisible.value = true;
  showSearch.value = false;
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
  margin-bottom: 15px;
}
.el-message {
  z-index: 9999 !important; /* 调整为更高的值 */
}
.el-form-item {
  padding-right: 30px; /* 控制输入框右侧与滚动条之间的空隙 */
}
</style>
