<script setup>
import { useRoute } from "vue-router";
import http from "@/api";
import { watch, ref, onBeforeMount } from "vue";
import {
  colorType,
  gene_aType,
  gene_bType,
  gene_cType,
  purposeType,
  rankType,
  sexType,
  stateType,
  varietyType
} from "@/assets/json/typeListJson";

const BASE_URL = import.meta.env.VITE_API_URL;

let route = useRoute();

let result = ref();
const params = route.query;
// watch(
//   () => route.query,
//   async () => {
//     console.log(params);
//     result.value = await http.post("/basic/basicinfo/detail", params).then(res => res.data.list);
//     console.log(result);
//   },
//   { immediate: true }
// );
onBeforeMount(async () => {
  console.log(params);
  result.value = await http.post("/basic/basicinfo/detail", params).then(res => res.data.list);
  console.log(result);
});
</script>
<template>
  <!-- <div>获取一下数据{{ result }}</div> -->
  <main v-if="result">
    <table>
      <thead>
        <tr>
          <th colspan="3">草地记录基本信息</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>草地编号</td>
          <td>{{ result.ele_num }}</td>
          <td rowspan="6">
            <el-image
              style="width: 200px; height: 185px"
              :src="`${BASE_URL}/basic/file/download/img?filename=${result.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${result.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
            <!-- <img :src="`${BASE_URL}/basic/file/download/img?filename=${result.img_positive}`" alt="正面照片" /></td> -->
          </td>
        </tr>
        <tr>
          <td>地块编号</td>
          <td>{{ result.pre_num }}</td>
        </tr>
        <tr>
          <td>作物类型</td>
          <td>{{ sexType.find(item => item.value === result.sex)?.label }}</td>
        </tr>
        <tr>
          <td>所属监测区域</td>
          <td>{{ result.house_name }}{{ result.hurdle_name }}</td>
        </tr>
        <tr>
          <td>原产地</td>
          <td>{{ result.manu_info_name }}</td>
        </tr>
        <tr>
          <td>用途</td>
          <td>
            {{
              purposeType.find(item => item.value === result.purpose)
                ? purposeType.find(item => item.value === result.purpose).label
                : "未分类"
            }}
          </td>
        </tr>
        <tr>
          <td>草地品系</td>
          <td>
            {{
              varietyType.find(item => item.value === result.variety)
                ? varietyType.find(item => item.value === result.variety).label
                : "未定义"
            }}
          </td>
          <td rowspan="6">
            <el-image
              style="width: 200px; height: 185px"
              :src="`${BASE_URL}/basic/file/download/img?filename=${result.img_left}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${result.img_left}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>左侧照片</div>
            <!-- <img :src="`${BASE_URL}/basic/file/download/img?filename=${result.img_left}`" alt="左侧照片" /> -->
          </td>
        </tr>
        <tr>
          <td>草地颜色</td>
          <td>
            {{
              colorType.find(item => item.value === result.color)
                ? colorType.find(item => item.value === result.color)?.label
                : "未填写"
            }}
          </td>
        </tr>
        <tr>
          <td>等级</td>
          <td>
            {{
              rankType.find(item => item.value === result.rank)
                ? rankType.find(item => item.value === result.rank)?.label
                : "未评定"
            }}
          </td>
        </tr>
        <tr>
          <td>种植日期</td>
          <td>{{ result.birth }}</td>
        </tr>
        <tr>
          <td>初始生物量</td>
          <td>{{ result.bir_weight }}(kg)</td>
        </tr>
        <tr>
          <td>生长月数</td>
          <td>{{ result.mon_age }}</td>
        </tr>
        <tr>
          <td>阶段生物量</td>
          <td>{{ result.wea_weight }}(kg)</td>
          <td rowspan="6">
            <el-image
              style="width: 200px; height: 185px"
              :src="`${BASE_URL}/basic/file/download/img?filename=${result.img_right}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${result.img_right}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>右侧照片</div>
            <!-- <img :src="`${BASE_URL}/basic/file/download/img?filename=${result.img_right}`" alt="右侧照片" /> -->
          </td>
        </tr>
        <tr>
          <td>上级地块编号</td>
          <td>{{ result.f_ele_num }}</td>
        </tr>
        <tr>
          <td>当前地块编号</td>
          <td>{{ result.m_ele_num }}</td>
        </tr>
        <tr>
          <td>多批基因</td>
          <td>
            {{
              gene_aType.find(item => item.value === result.gene_a)
                ? gene_aType.find(item => item.value === result.gene_a)?.label
                : "暂空"
            }}
          </td>
        </tr>
        <tr>
          <td>抗病基因</td>
          <td>
            {{
              gene_bType.find(item => item.value === result.gene_b)
                ? gene_bType.find(item => item.value === result.gene_b)?.label
                : "暂空"
            }}
          </td>
        </tr>
        <tr>
          <td>待定基因</td>
          <td>
            {{
              gene_cType.find(item => item.value === result.gene_c)
                ? gene_cType.find(item => item.value === result.gene_c)?.label
                : "暂空"
            }}
          </td>
        </tr>
        <tr>
          <td>添加人</td>
          <td>{{ result.f_staff }}</td>
        </tr>
        <tr>
          <td>添加时间</td>
          <td>{{ result.f_date }}</td>
        </tr>
        <tr>
          <td>状态</td>
          <td>{{ stateType.find(item => item.value === result.state)?.label }}</td>
        </tr>
        <tr>
          <td>备注</td>
          <td>{{ result.note }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>
<style scoped>
main {
  width: fit-content;
  margin: 0 auto;
}
img {
  width: 200px;
  height: 185px;
  object-fit: contain;
}
table {
  width: 610px;
  table-layout: fixed;
  border-collapse: collapse;
  border: 1px solid #cccccc;
}
td {
  height: 35px;
  font-size: 14px;
  color: #606266;
  border: 1px solid #cccccc;
}
td:nth-child(1),
td:nth-child(2) {
  padding-left: 10px;
}
th {
  height: 50px;
  font-size: 20px;
}
tr:hover {
  background-color: #f5f7fa;
  transition: background-color 0.25s ease;
}
td > div:last-child {
  font-size: small;
  text-align: center;
}
.image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
}
</style>
