// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "/analysis";
// 获取列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/daily_sheep_asset`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
// 新增
export const updateSheepAsset = () => {
  return http.post(PORT1 + `/daily_sheep_asset/update`);
};
// 导出数据
export const exportSheepInfo = params => {
  return http.download(PORT1 + `/daily_sheep_asset/export`, params);
};

// 新增
export const updateDailyIncome = () => {
  return http.post(PORT1 + `/daily_income/update`);
};

// 编辑
export const editManu = params => {
  return http.post(PORT1 + `/inventory/edit`, params);
};

// 删除
export const delManu = params => {
  return http.post(PORT1 + `/inventory/del`, params);
};
