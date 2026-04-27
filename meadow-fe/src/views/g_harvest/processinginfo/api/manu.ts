import http from "@/api";

// TODO: Backend route for processinginfo is missing.
// Using segmentinfo table endpoint as a placeholder until backend is implemented.

// 获取记录列表
export const getManuList = params => {
  const result = http.post(`/g_harvest/segmentinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(`/g_harvest/segmentinfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(`/g_harvest/segmentinfo/edit`, params);
};
