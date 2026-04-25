// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";

const PORT1 = "analysis";
// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT1 + `/grass_assetinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

export const updateGrassAsset = () => {
  return http.post(PORT1 + `/grass_assetinfo/update`);
};

export const commitUpdateAsset = params => {
  return http.post(PORT1 + `/grass_assetinfo/commit_update`, params);
};

// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/grass_assetinfo/export`, params);
};
//获取监测目标信息
export const getEweGrass = params => {
  const result = http.post(PORT1 + `/rutinfo/get_ewegrass`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};
