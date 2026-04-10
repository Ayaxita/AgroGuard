import { PORT3 } from "@/api/config/servicePort";
import http from "@/api";

// 获取记录列表
export const getManuList = params => {
  const result = http.post(PORT3 + `/immunizationinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addManu = params => {
  return http.post(PORT3 + `/immunizationinfo/add`, params);
};

// 编辑记录
export const editManu = params => {
  return http.post(PORT3 + `/immunizationinfo/edit`, params);
};
// 编辑记录
export const delinfo = params => {
  return http.post(PORT3 + `/immunizationinfo/del`, params);
};

// 导出数据
export const exportSheepInfo = params => {
  return http.download(PORT3 + `/immunizationinfo/export`, params);
};

export const delImmunizationinfo = params => {
  const promises = params.map(item => {
    return delinfo(item);
  });
  // console.log("所有的promise", promises);
  return Promise.all(promises)
    .then(() => {
      return 200;
    })
    .catch(err => {
      console.log("标记淘汰出错");
      throw err;
    });
};
