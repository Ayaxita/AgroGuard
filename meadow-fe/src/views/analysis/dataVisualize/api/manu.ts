import http from "@/api";
const PORT6 = "/analysis";
//获取每月
export const getTest = params => {
  const result = http.post(PORT6 + `/dataVisualize`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//获取整月
export const getTestMonth = params => {
  const result = http.post(PORT6 + `/monthlyDataVisualize`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//获取每季
export const getTestQuarter = params => {
  const result = http.post(PORT6 + `/quarterlyDataVisualize`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
//获取每年
export const getTestYear = params => {
  const result = http.post(PORT6 + `/annualDataVisualize`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
