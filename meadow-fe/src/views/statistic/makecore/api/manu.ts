// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
const PORT1 = "/statistic";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/makescore`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
// export const addManu = params => {
//   return http.post(PORT1 + `/seedlinginfo/add`, params);
// };

// 编辑
export const editManu = params => {
  return http.post(PORT1 + `/makescore/edit`, params);
};
