import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT2 = "/colony";
// 获取列表
export const getHouseList = params => {
  const result = http.post(PORT2 + `/houseinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
// 获取记录列表
export const getCutinfoList = params => {
  const result = http.post(PORT1 + `/harvestinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addCutinfo = params => {
  return http.post(PORT1 + `/harvestinfo/add`, params);
};

// 编辑记录
export const editCutinfo = params => {
  return http.post(PORT1 + `/harvestinfo/edit`, params);
};

// 删除记录
export const delCutinfo = params => {
  return http.post(PORT1 + `/harvestinfo/del`, params);
};
