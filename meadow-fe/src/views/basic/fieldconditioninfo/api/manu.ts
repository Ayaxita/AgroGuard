// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "/basic";
interface info_data {
  list: Array<any>;
  pageNum: number;
  pageSize: number;
  total: number;
}
// 获取记录列表
export const getBreederConditionInfoList = params => {
  const result = http.post<info_data>(PORT1 + `/fieldconditioninfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addBreederConditionInfo = params => {
  return http.post(PORT1 + `/fieldconditioninfo/add`, params);
};

// 编辑记录
export const editBreederConditionInfo = params => {
  return http.post(PORT1 + `/fieldconditioninfo/edit`, params);
};

// 删除
export const delManu = params => {
  return http.post(PORT1 + `/fieldconditioninfo/del`, params);
};
//获取能添加母本体况信息的优质记录信息
export const getGoodgrass = params => {
  const result = http.post(PORT1 + `/fieldconditioninfo/get_Goodgrass`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

//获取同羔数
export const getWith_births = params => {
  const result = http.post(PORT1 + `/fieldconditioninfo/getWith_births`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
