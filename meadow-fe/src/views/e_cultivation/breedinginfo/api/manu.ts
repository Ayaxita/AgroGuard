// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "e_cultivation";
// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/breedinginfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//判断近亲相交
export const judgeInBreed = params => {
  const result = http.post(PORT1 + `/breedinginfo/judge_inbreed`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
// 新增记录
export const addManu = params => {
  return http.post(PORT1 + `/breedinginfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT1 + `/breedinginfo/edit`, params);
};
// 删除记录
export const delManu = params => {
  return http.post(PORT1 + `/breedinginfo/del`, params);
};
// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/breedinginfo/export`, params);
};
