// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "/colony";
// 获取列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/hurdleinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增
export const addManu = params => {
  return http.post(PORT1 + `/hurdleinfo/add`, params);
};

// 编辑
export const editManu = params => {
  return http.post(PORT1 + `/hurdleinfo/edit`, params);
};
// 删除
export const delManu = params => {
  return http.post(PORT1 + `/hurdleinfo/del`, params);
};
// 初始化house
export const initHouse = () => {
  return http.post(PORT1 + `/hurdleinfo/initHouse`);
};
// 清点栏舍数量
export const updateHurdleNumber = () => {
  return http.post(PORT1 + `/hurdleinfo/updateHurdleNumber`);
};
// 消毒
export const disinfectHurdle = params => {
  return http.post(PORT1 + `/hurdleinfo/disinfectHurdle`, params);
};
//合并
export const setHurdle = params => {
  return http.post(PORT1 + `/hurdleinfo/set`, params);
};
//拆分
export const unsealHurdle = params => {
  return http.post(PORT1 + `/hurdleinfo/unseal`, params);
};
