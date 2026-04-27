// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
const PORT1 = "propagation";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/post_harvestinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(PORT1 + `/post_harvestinfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT1 + `/post_harvestinfo/edit`, params);
};
// 删除记录
export const delManu = params => {
  return http.post(PORT1 + `/post_harvestinfo/del`, params);
};
// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/post_harvestinfo/export`, params);
};

//获取可添加产后信息的记录
export const getEwe = params => {
  const result = http.post(PORT1 + `/post_harvestinfo/get_ewe`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//获取可添加关联信息的记录
export const getRam = params => {
  const result = http.post(PORT1 + `/post_harvestinfo/get_ram`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
// 查找记录是否在批次关联表中有记录
export const searchEweGrass = params => {
  const result = http.post(PORT1 + `/post_harvestinfo/search_ewe_grass`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//添加关联信息到批次关联表
export const addBreeding = params => {
  return http.post(PORT1 + `/post_harvestinfo/add_breeding`, params);
};
//获取批次记录信息
export const getLamb = params => {
  const result = http.post(PORT1 + `/post_harvestinfo/getlamb`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
