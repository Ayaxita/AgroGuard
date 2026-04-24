<template>
  <div class="economic-analysis">
    <div class="left-section">
      <ProfitChart :chart-data="incomeMainData" title="利润分布" color="#FF5733" />
    </div>

    <!-- 顶部汇总卡片 -->
    <div class="right-section">
      <el-card class="summary-card">
        <el-table :data="summaryData" style="width: 100%">
          <el-table-column prop="income" label="收入（元）" />
          <el-table-column prop="outcome" label="支出（元）" />
          <el-table-column prop="assets" label="草地资产（元）" />
          <el-table-column prop="weekly" label="周收益（元）" class-name="warning-column" />
        </el-table>
      </el-card>
    </div>

    <div class="main-content">
      <!-- 左侧资产图表 -->
      <el-card class="assets-section">
        <div class="chart-container">
          <LineChart :chart-data="sheepAssetsData" title="草地库存资产" color="#8A2BE2" />
        </div>
        <div class="chart-container">
          <LineChart :chart-data="inventoryAssetsData" title="物料库存资产" color="#FF4500" />
        </div>
      </el-card>

      <!-- 右侧收支图表 -->
      <div class="inout-section">
        <!-- 收入部分 -->
        <el-card class="income-section">
          <h2 class="section-title green">收 入 统 计</h2>
          <div class="chart-group">
            <LineChart :chart-data="incomeMainData" title="草地记录销售收入" color="#FF5733" />
            <LineChart :chart-data="incomeByproductData" title="草地副产品收入" color="#4CAF50" />
          </div>
        </el-card>

        <!-- 支出部分 -->
        <el-card class="outcome-section">
          <h2 class="section-title orange">支 出 统 计</h2>
          <div class="chart-group">
            <MultiLineChart :chart-data="directCostData" title="直接费用" :colors="directColors" />
            <LineChart :chart-data="indirectCostData" title="间接费用" color="#6A5ACD" />
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import LineChart from "../components/LineChart.vue";
import ProfitChart from "../components/ProfitChart.vue";
// import MultiLineChart from "./components/MultiLineChart.vue";

// 汇总数据
const summaryData = ref([
  {
    income: 222493,
    outcome: 91198.74,
    assets: -140900,
    weekly: -9605.74
  }
]);

// 资产数据
const sheepAssetsData = ref({
  xData: ["2025/1/1", "2025/1/2", "2025/1/3", "2025/1/4", "2025/1/5", "2025/1/6", "2025/1/7"],
  series: [
    /* 填充实际数据 */
  ]
});

const inventoryAssetsData = ref({
  xData: ["2025/1/1", "2025/1/2", "2025/1/3", "2025/1/4", "2025/1/5", "2025/1/6", "2025/1/7"],
  series: [
    /* 填充实际数据 */
  ]
});

// 收入数据
const incomeMainData = ref({
  xData: ["2025/1/1", "2025/1/2", "2025/1/3", "2025/1/4", "2025/1/5", "2025/1/6", "2025/1/7"],
  series: [
    /* 填充实际数据 */
  ]
});

const incomeByproductData = ref({
  xData: ["2025/1/1", "2025/1/2", "2025/1/3", "2025/1/4", "2025/1/5", "2025/1/6", "2025/1/7"],
  series: [
    /* 填充实际数据 */
  ]
});

// 支出数据
const directCostData = ref({
  xData: ["2025/1/1", "2025/1/2", "2025/1/3", "2025/1/4", "2025/1/5", "2025/1/6", "2025/1/7"],
  series: [
    { name: "直接费用", data: [] },
    { name: "草地投入费用", data: [] },
    { name: "人工费用", data: [] }
  ]
});

// 样式配置
const directColors = ref(["#FFD700", "#FF6347", "#32CD32"]);
</script>

<style scoped lang="scss">
.economic-analysis {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: #f5f7f9;

  /* 左右两部分均分宽度，可根据实际需求调整比例 */
  .left-section,
  .right-section {
    flex: 1;
  }
  .summary-card {
    margin-bottom: 20px;
    :deep(.warning-column) {
      font-weight: bold;
      color: var(--el-color-danger);
    }
  }
  .main-content {
    display: flex;
    gap: 20px;
    .assets-section {
      flex: 0 0 30%;
      .chart-container {
        height: 50%;
        margin: 10px 0;
      }
    }
    .inout-section {
      flex: 1;
      .income-section,
      .outcome-section {
        margin-bottom: 20px;
        .chart-group {
          display: flex;
          gap: 20px;
          > div {
            flex: 1;
            height: 400px;
          }
        }
      }
    }
  }
}
.section-title {
  padding: 10px;
  margin: 20px 0;
  font-size: 24px;
  text-align: center;
  border-radius: 8px;
  &.green {
    background: linear-gradient(45deg, #e6f7e0, #c8e6c9);
  }
  &.orange {
    background: linear-gradient(45deg, #fff3e0, #ffe0b2);
  }
}
</style>
