// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "analysis";
// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/sheep_assetinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

export const updateSheepAsset = () => {
  return http.post(PORT1 + `/sheep_assetinfo/update`);
};

export const commitUpdateAsset = params => {
  return http.post(PORT1 + `/sheep_assetinfo/commit_update`, params);
};

// 导出数据
export const exportSheepInfo = params => {
  return http.download(PORT1 + `/sheep_assetinfo/export`, params);
};
//获取监测目标信息
export const getEweSheep = params => {
  const result = http.post(PORT1 + `/rutinfo/get_ewesheep`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
