// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
const PORT1 = "e_breed";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/postnatalinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(PORT1 + `/postnatalinfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT1 + `/postnatalinfo/edit`, params);
};
// 删除记录
export const delManu = params => {
  return http.post(PORT1 + `/postnatalinfo/del`, params);
};
// 导出数据
export const exportSheepInfo = params => {
  return http.download(PORT1 + `/postnatalinfo/export`, params);
};

//获取可添加产后信息的记录
export const getEwe = params => {
  const result = http.post(PORT1 + `/postnatalinfo/get_ewe`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//获取可添加关联信息的记录
export const getRam = params => {
  const result = http.post(PORT1 + `/postnatalinfo/get_ram`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
// 查找记录是否在批次关联表中有记录
export const searchEweSheep = params => {
  const result = http.post(PORT1 + `/postnatalinfo/search_ewe_sheep`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//添加关联信息到批次关联表
export const addBreeding = params => {
  return http.post(PORT1 + `/postnatalinfo/add_breeding`, params);
};
//获取批次记录信息
export const getLamb = params => {
  const result = http.post(PORT1 + `/postnatalinfo/getlamb`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
