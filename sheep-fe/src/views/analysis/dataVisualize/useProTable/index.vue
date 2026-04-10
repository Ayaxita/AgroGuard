<template>
  <div class="dashboard-container">
    <!-- 时间选择按钮 -->
    <div class="time-selector">
      <el-button @click="getData">查看日度</el-button>
      <el-button @click="getMonth">查看月度</el-button>
      <el-button @click="getQuarter">查看季度</el-button>
      <el-button @click="getYear">查看年度</el-button>
      <div>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          class="custom-date-picker"
          style="width: 200px; margin-left: 10px"
        />
      </div>
    </div>

    <!-- 上半部分 -->
    <div class="top-section">
      <div class="chart-box left">
        <div ref="profitChart" style="height: 400px"></div>
      </div>

      <div class="table-box right">
        <el-table :data="tableData" height="400" style="width: 100%" stripe border>
          <el-table-column
            prop="date"
            label="记录日期"
            width="120"
            :formatter="
              row => {
                const date = new Date(row.date);
                switch (currentGranularity) {
                  case 'month':
                    return date.toISOString().slice(0, 7);
                  case 'quarter':
                    // 直接返回预存的季度字符串
                    return row.quarterStr;
                  case 'year':
                    return date.getFullYear();
                  default:
                    return date.toLocaleDateString();
                }
              }
            "
          />
          <el-table-column prop="income_total" label="防治收益(元)" width="120" />
          <el-table-column prop="expense_total" label="防治投入(元)" width="120" />
          <el-table-column prop="sub_sheep_asset" label="风险资产变化(元)" width="140" />
          <el-table-column prop="profit" label="净收益(元)" width="120" />
        </el-table>
      </div>
    </div>

    <!-- 下半部分 -->
    <div class="bottom-section">
      <div class="left-stock">
        <div ref="sheepStockChart" style="height: 300px; margin-bottom: 20px"></div>
        <div ref="materialStockChart" style="height: 300px"></div>
      </div>

      <div class="right-stats">
        <div ref="salesIncomeChart" style="height: 300px; margin-bottom: 20px"></div>
        <div ref="directExpenseChart" style="height: 300px; margin-bottom: 20px"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import * as echarts from "echarts";
import { getTest, getTestMonth, getTestQuarter, getTestYear } from "../api/manu";
import axios from "axios";

const profitChart = ref(null);
const sheepStockChart = ref(null);
const materialStockChart = ref(null);
const salesIncomeChart = ref(null);
const directExpenseChart = ref(null);

const currentGranularity = ref("day"); // 初始化时间粒度

const colorPalette = [
  "#5470C6",
  "#91CC75",
  "#FAC858",
  "#EE6666",
  "#73C0DE",
  "#3BA272",
  "#FC8452",
  "#9A60B4",
  "#EA7CCC",
  "#27727B",
  "#FADB61",
  "#6E7074"
];

const tableData = ref([]);

// 数据处理方法：转换日期并针对季度数据保存原始字符串
const processData = (data, granularity) => {
  currentGranularity.value = granularity;
  tableData.value = data.map(item => {
    let date;
    let quarterStr = "";
    switch (granularity) {
      case "month":
        date = new Date(item.date + "-01"); // 月份数据补全日期
        break;
      case "quarter":
        const [year, q] = item.date.split("-Q");
        date = new Date(year, (parseInt(q) - 1) * 3, 1);
        quarterStr = item.date; // 保存原始季度字符串
        break;
      case "year":
        date = new Date(item.date, 0, 1);
        break;
      default:
        date = new Date(item.date);
    }
    return {
      ...item,
      date: date.getTime(), // 存储时间戳供图表使用
      quarterStr, // 针对季度显示
      sub_sheep_asset: item.sub_sheep_asset || 0
    };
  });

  // 销毁旧图表并重新初始化
  charts.forEach(chart => {
    chart.dispose();
  });
  charts = [];
  initCharts();
};

const getMonth = async () => {
  try {
    const response = await getTestMonth();
    if (response.data && response.data.length > 0) {
      processData(response.data, "month");
    }
  } catch (error) {
    console.error("获取月度数据失败:", error);
  }
};

const getQuarter = async () => {
  try {
    const response = await getTestQuarter();
    if (response.data && response.data.length > 0) {
      processData(response.data, "quarter");
    }
  } catch (error) {
    console.error("获取季度数据失败:", error);
  }
};

const getData = async () => {
  try {
    currentGranularity.value = "day";
    const response = await getTest();
    tableData.value = response.data;
    initCharts();
  } catch (error) {
    console.error("获取数据失败:", error);
  }
};

const getYear = async () => {
  try {
    const response = await getTestYear();
    if (response.data && response.data.length > 0) {
      processData(response.data, "year");
    }
  } catch (error) {
    console.error("获取年度数据失败:", error);
  }
};

const createTimeChartOption = (title, series) => {
  // 根据数据计算 x 轴的标签数组，每个标签都对应 tableData 中的一个数据点
  const xAxisData = tableData.value.map(item => {
    const date = new Date(item.date);
    switch (currentGranularity.value) {
      case "month":
        // 显示月份（两位数）
        return (date.getMonth() + 1).toString().padStart(2, "0");
      case "quarter":
        // 显示季度，例如 "Q1"
        return "Q" + (Math.floor(date.getMonth() / 3) + 1);
      case "year":
        // 显示年份
        return date.getFullYear();
      default:
        // 日度：显示具体日期（可改为你需要的格式，比如 "MM-DD"）
        return date.getDate();
    }
  });

  return {
    color: colorPalette,
    title: {
      text: title,
      left: "center",
      textStyle: {
        fontSize: 16,
        color: "#333",
        fontWeight: "normal"
      }
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow"
      }
    },
    legend: {
      type: "scroll",
      top: 30,
      textStyle: {
        color: "#666",
        fontSize: 12
      },
      pageTextStyle: {
        color: "#666"
      },
      pageIconColor: "#666",
      pageIconInactiveColor: "#bbb",
      padding: [0, 50]
    },
    grid: {
      top: 80,
      bottom: 100,
      containLabel: true
    },
    // 使用 category 类型，这样 x 轴刻度数就正好等于数据点数
    xAxis: {
      type: "category",
      data: xAxisData,
      axisLabel: {
        color: "#666",
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: "#999",
          width: 1
        }
      },
      splitLine: {
        show: false
      }
    },
    yAxis: {
      type: "value",
      axisLabel: {
        color: "#666",
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: "#999",
          width: 1
        }
      },
      splitLine: {
        lineStyle: {
          color: "#eee",
          type: "dashed"
        }
      }
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow"
      },
      formatter: function (params) {
        const index = params[0].dataIndex;
        const fullDate = tableData.value[index].date; // 获取完整日期
        let tooltipText = `<b>${fullDate}</b><br/>`;
        params.forEach(param => {
          tooltipText += `${param.marker} ${param.seriesName}: ${param.value}<br/>`;
        });
        return tooltipText;
      }
    },
    // 注意：这里 series 数据需要调整为仅包含 y 值，
    // 顺序上与 xAxis.data 中的标签一一对应
    series: series.map(item => ({
      ...item,
      type: "line",
      smooth: true,
      showSymbol: false,
      lineStyle: {
        width: 2,
        cap: "round"
      },
      emphasis: {
        focus: "series",
        itemStyle: {
          borderWidth: 2
        }
      }
    }))
  };
};

const initChart = (chartRef, title, series) => {
  const option = createTimeChartOption(title, series);
  option.legend.data = series.map(s => s.name);
  const chart = echarts.init(chartRef.value);
  chart.setOption(option);
  return chart;
};

let charts = [];
const initCharts = () => {
  charts = [
    // 只传入 y 值，x轴数据由 getXAxisData() 生成
    initChart(profitChart, "病虫害趋势分析", [{ name: "净收益", data: tableData.value.map(i => i.profit) }]),
    initChart(sheepStockChart, "草地风险资产趋势", [{ name: "风险资产", data: tableData.value.map(i => i.sheep_asset) }]),
    initChart(materialStockChart, "防护物资库存趋势", [{ name: "库存价值", data: tableData.value.map(i => i.stock_asset) }]),
    initChart(salesIncomeChart, "防治收益统计", [
      { name: "重点地块", data: tableData.value.map(i => i.income_sales.breeding_sheep.value) },
      { name: "生长期地块", data: tableData.value.map(i => i.income_sales.fattening_sheep.value) },
      { name: "幼苗期地块", data: tableData.value.map(i => i.income_sales.lamb.value) },
      { name: "淘汰地块", data: tableData.value.map(i => i.income_sales.other_sheep.value) },
      { name: "草地残渣", data: tableData.value.map(i => i.income_byproducts.dung) },
      { name: "采收产物", data: tableData.value.map(i => i.income_byproducts.wool) },
      { name: "地表覆盖物", data: tableData.value.map(i => i.income_byproducts.skin) },
      { name: "有机肥", data: tableData.value.map(i => i.income_byproducts.manure) },
      { name: "草地投入", data: tableData.value.map(i => i.income_byproducts.feed) },
      { name: "草地副产品", data: tableData.value.map(i => i.income_byproducts.producted) },
      { name: "其他", data: tableData.value.map(i => i.income_byproducts.other) },
      {
        name: "防治总收益",
        data: tableData.value.map(i => [
          i.income_sales.breeding_sheep.value +
            i.income_sales.fattening_sheep.value +
            i.income_sales.lamb.value +
            i.income_sales.other_sheep.value
        ])
      }
    ]),
    initChart(directExpenseChart, "防治投入统计", [
      { name: "种苗购买费", data: tableData.value.map(i => i.expense_direct.detail.buysheep) },
      { name: "草地投入费", data: tableData.value.map(i => i.expense_direct.detail.forage) },
      { name: "精准投入费", data: tableData.value.map(i => i.expense_direct.detail.fine_fodder) },
      { name: "防护费", data: tableData.value.map(i => i.expense_direct.detail.vaccine) },
      { name: "药物费", data: tableData.value.map(i => i.expense_direct.detail.medicine) },
      { name: "人工费", data: tableData.value.map(i => i.expense_direct.detail.labor) },
      { name: "直接总费用", data: tableData.value.map(i => i.expense_direct.total) },
      { name: "间接总费用", data: tableData.value.map(i => i.expense_indirect.total) }
    ])
  ];
};

const handleResize = () => {
  charts.forEach(chart => chart.resize());
};

onMounted(() => {
  getData();
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  charts.forEach(chart => chart.dispose());
  charts = [];
});
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding: 20px;
  background: #f8f9fa;
}
.time-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
.chart-box,
.table-box {
  flex: 1;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 8%);
  transition: box-shadow 0.2s ease;
}
.chart-box:hover,
.table-box:hover {
  box-shadow: 0 4px 16px rgb(0 0 0 / 12%);
}
.bottom-section {
  display: flex;
  gap: 20px;
}
.left-stock {
  display: flex;
  flex: 0 0 35%;
  flex-direction: column;
  gap: 20px;
}
.right-stats {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
}
.el-table {
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgb(0 0 0 / 8%);
}
.echarts {
  width: 100% !important;
  height: 100% !important;
}
</style>
