// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "/analysis";
// 获取列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/daily_grass_asset`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
// 新增
export const updateGrassAsset = () => {
  return http.post(PORT1 + `/daily_grass_asset/update`);
};
// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/daily_grass_asset/export`, params);
};

// 新增
export const updateDailyIncome = () => {
  return http.post(PORT1 + `/daily_grass_asset/update`);
};

// 编辑
export const editManu = params => {
  return http.post(PORT1 + `/daily_grass_asset/edit`, params);
};

// 删除
export const delManu = params => {
  return http.post(PORT1 + `/daily_grass_asset/del`, params);
};
