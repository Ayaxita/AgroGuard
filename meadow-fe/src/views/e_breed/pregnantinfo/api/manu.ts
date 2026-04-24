// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
const PORT1 = "e_breed";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/pregnantinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(PORT1 + `/pregnantinfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT1 + `/pregnantinfo/edit`, params);
};
// 删除记录
export const delManu = params => {
  return http.post(PORT1 + `/pregnantinfo/del`, params);
};
// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/pregnantinfo/export`, params);
};
