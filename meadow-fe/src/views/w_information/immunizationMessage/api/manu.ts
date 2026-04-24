import { PORT5 } from "@/api/config/servicePort";
import http from "@/api";
interface Immthresholdset {
  id: number;
  vaccine_id: number;
  threshold: number;
  threshold_mon: number;
  threshold_year: number;
}
interface ThresholdResponse {
  list: any;
  data: Immthresholdset[];
}
// 获取预警信息列表
export const getManuList = params => {
  const result = http.post(PORT5 + `/immunizationMessageinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//获取阈值列表
export const getThresholdeinfo = () => {
  const result = http.post<ThresholdResponse>(PORT5 + `/thresholdsetMessageinfo`);
  result.then(resp => {
    console.log("返回的列表数据", resp);
  });
  return result;
};
//编辑阈值列表
export const editThresholdeinfo = params => {
  return http.post<ThresholdResponse>(PORT5 + `/thresholdsetMessageinfo/edit`, params);
};
//更新预警信息
export const updateWarnMessage = () => {
  const result = http.post(PORT5 + `/thresholdsetMessageinfo/update`);
};
// 新增记录
// export const addManu = params => {
//   return http.post(PORT3 + `/immunizationinfo/add`, params);
// };

// 编辑记录
// export const editManu = params => {
//   return http.post(PORT3 + `/immunizationinfo/edit`, params);
// };
// 删除记录
// export const delinfo = params => {
//   return http.post(PORT3 + `/immunizationinfo/del`, params);
// };

// 导出数据
// export const exportImmunizationInfo = params => {
//   return http.download(PORT3 + `/immunizationinfo/export`, params);
// };
