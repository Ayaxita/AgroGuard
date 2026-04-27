import { PORT3 } from "@/api/config/servicePort";
import http from "@/api";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT3 + `/damageinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(PORT3 + `/damageinfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT3 + `/damageinfo/edit`, params);
};

// 删除记录
export const delManu = params => {
  return http.post(PORT3 + `/damageinfo/del`, params);
};
// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT3 + `/damageinfo/export`, params);
};
