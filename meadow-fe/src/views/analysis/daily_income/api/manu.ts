// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "/analysis";
// 获取列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/daily_income`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增
export const updateDailyIncome = () => {
  return http.post(PORT1 + `/daily_income/update`);
};

export const updateSelectDailyIncome = params => {
  return http.post(PORT1 + `/daily_income/selectupdate`, params);
};

//在标记销售之后，已经插入数据后去调用
export const commitUpdateDailyIncome = params => {
  return http.post(PORT1 + `/daily_income/commit_update`, params);
};

// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/daily_income/export`, params);
};
// 编辑
export const editManu = params => {
  return http.post(PORT1 + `/daily_income/edit`, params);
};

// 删除
export const delManu = params => {
  return http.post(PORT1 + `/daily_income/del`, params);
};
