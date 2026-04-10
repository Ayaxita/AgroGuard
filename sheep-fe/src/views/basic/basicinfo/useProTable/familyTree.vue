<template>
  <div class="card content-box">
    <!-- <span class="text">我是 ProTable 详情页，属于 ProTable 下面的子集 🍓🍇🍈🍉</span>
    <span class="text">params:{{ route.params }}</span>
    <span class="text">query:{{ route.query }}</span> -->
    <div class="family-tree-container">
      <el-row>
        <el-col :span="6">
          <div class="family-tree-item">
            <div>祖父：{{ data.grandfather?.ele_num }}</div>
            <div>播种日期：{{ data.grandfather?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.grandfather?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.grandfather?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.grandfather?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="family-tree-item">
            <div>祖母：{{ data.grandmother?.ele_num }}</div>
            <div>播种日期：{{ data.grandmother?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.grandmother?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.grandmother?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.grandmother?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="family-tree-item">
            <div>外祖父：{{ data.maternal_grandfather?.ele_num }}</div>
            <div>播种日期：{{ data.maternal_grandfather?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.maternal_grandfather?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.maternal_grandfather?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.maternal_grandfather?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="family-tree-item">
            <div>外祖母：{{ data.maternal_grandmother?.ele_num }}</div>
            <div>播种日期：{{ data.maternal_grandmother?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.maternal_grandmother?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.maternal_grandmother?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.maternal_grandmother?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <div class="family-tree-item">
            <div>父亲：{{ data.father?.ele_num }}</div>
            <div>播种日期：{{ data.father?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.father?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.father?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.father?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="family-tree-item">
            <div>母亲：{{ data.mother?.ele_num }}</div>
            <div>播种日期：{{ data.mother?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.mother?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.mother?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.mother?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <div class="family-tree-item">
            <div>种植区：{{ data.selected_sheep?.ele_num }}</div>
            <div>播种日期：{{ data.selected_sheep?.birth }}</div>
            <div>草地类型：{{ varietyType.find(item => item.value === data.selected_sheep?.variety)?.label }}</div>
            <el-image
              style="width: 100px; height: 100px"
              :src="BASE_URL + `/basic/file/download/img?filename=${data.selected_sheep?.img_positive}`"
              :zoom-rate="1.2"
              :max-scale="7"
              :min-scale="0.2"
              :preview-src-list="[`${BASE_URL}/basic/file/download/img?filename=${data.selected_sheep?.img_positive}`]"
              :initial-index="4"
              fit="contain"
            >
              <!-- 可通过slot = error可自定义加载失败内容 -->
              <template #error>
                <div class="image-slot">空</div>
              </template>
            </el-image>
            <div>正面照片</div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup name="useProTableDetailFamilyTree">
import { useRoute } from "vue-router";
import { getSheepFamilyTree } from "../api/sheep";
import { onBeforeMount, onMounted, ref } from "vue";
import { varietyType } from "@/assets/json/typeListJson";
const route = useRoute();
const data = ref({});

const BASE_URL = import.meta.env.VITE_API_URL;
const getSheepFamilyTreeData = async () => {
  const res = await getSheepFamilyTree({
    id: route.params.id
  });
  data.value = res;
  // console.log(res);
  // console.log(res.maternal_grandfather?.ele_num);
};

onBeforeMount(() => {
  getSheepFamilyTreeData();
});
</script>

<style lang="css" scoped>
.family-tree-container {
  width: 100%;
  height: 100%;
}
.family-tree-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.family-tree-item > div:first-child {
  font-size: large;
  font-weight: 700;
}
.family-tree-item > div:last-child {
  font-size: small;
}
div.el-col {
  border: 1px solid var(--el-border-color);
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
