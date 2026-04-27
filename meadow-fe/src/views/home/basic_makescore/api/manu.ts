import http from "@/api";

const PORT1 = "/statistic/makescore";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(PORT1 + `/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT1 + `/edit`, params);
};
