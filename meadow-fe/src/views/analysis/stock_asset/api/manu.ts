// import { PORT6 } from "@/api/config/servicePort";
import http from "@/api";
const PORT6 = "/analysis";
// 获取物资库存信息列表
export const getManuList = params => {
  const result = http.post(PORT6 + `/daily_stocksheet`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增日报表信息
// export const addManu = params => {
//   return http.post(PORT6 + `/daily_report/add`, params);
// };

// 编辑日报表信息
// export const editManu = params => {
//   return http.post(PORT6 + `/daily_report/edit`, params);
// };

export const searchDate = params => {
  const result = http.post(PORT6 + `/daily_stocksheet/searchDate`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

//更新预警信息
export const updatestocksheet = () => {
  const result = http.post(PORT6 + `/daily_stocksheet/update`);
};
// 导出数据
export const exportStockasset = params => {
  return http.download(PORT6 + `/daily_stocksheet/export`, params);
};
// 删除记录
// export const delinfo = params => {
//   return http.post(PORT3 + `/immunizationinfo/del`, params);
// };

// 导出数据
// export const exportImmunizationInfo = params => {
//   return http.download(PORT3 + `/immunizationinfo/export`, params);
// };
