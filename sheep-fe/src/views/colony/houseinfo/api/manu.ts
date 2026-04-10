// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "/colony";
// 获取列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/houseinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增
export const addManu = params => {
  return http.post(PORT1 + `/houseinfo/add`, params);
};

// 编辑
export const editManu = params => {
  return http.post(PORT1 + `/houseinfo/edit`, params);
};

// 删除
export const delManu = params => {
  // console.log(params);
  return http.post(PORT1 + `/houseinfo/del`, params);
};

// 清点棚舍数量
export const updateHouseNumber = () => {
  return http.post(PORT1 + `/houseinfo/updateHouseNumber`);
};
