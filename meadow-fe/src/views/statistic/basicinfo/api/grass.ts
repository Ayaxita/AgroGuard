// import { PORT1 } from "@/api/config/servicePort";
import http from "@/api";
import axios from "axios";

const PORT1 = "/statistic";

// 获取记录列表
export const getGrassList = params => {
  const result = http.post(PORT1 + `/basicinfo`, params);
  result.then(resp => console.log("返回的列表数据", resp));
  return result;
};

// 新增记录
export const addGrass = params => {
  return http.post(PORT1 + `/basicinfo/add`, params);
};
// 新增免疫信息
export const addImmunization = params => {
  return http.post(PORT1 + `/basicinfo/addImmunization`, params);
};

// 编辑记录
export const editGrass = params => {
  return http.post(PORT1 + `/basicinfo/edit`, params);
};

// 获取记录档案
export const getGrassFamilyTree = params => {
  return http.post(PORT1 + `/basicinfo/familyTree`, params);
};

// 标记死亡
export const markGrassDeath = params => {
  return http.post(PORT1 + `/basicinfo/markGrassDeath`, params);
};

// 标记售出
export const markGrassSale = params => {
  return http.post(PORT1 + `/basicinfo/markGrassSale`, params);
};

//批量标记淘汰
export const markGrassDieOut = params => {
  const promises = params.map(item => {
    return editGrass(item);
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

// 导出数据
export const exportGrassInfo = params => {
  return http.download(PORT1 + `/basicinfo/export`, params);
};

// 批量添加记录模板
export const BatchAddGrassTemp = params => {
  return axios({
    url: import.meta.env.VITE_API_URL + PORT1 + `/basicinfo/import_template`,
    method: "post",
    data: params,
    headers: {
      "Content-Type": "multipart/form-data"
    },
    responseType: "blob"
  });
  // return http.post(PORT1 + `/basicinfo/import_template`, params);
};

// 批量添加记录
export const BatchAddGrass = params => {
  return http.post(PORT1 + `/basicinfo/import`, params);
};

//更新月龄
export const updateMonAge = () => {
  //更新月龄的前端超时时间是120000，不能决定是否成功
  return http.post(PORT1 + `/basicinfo/updateMonAge`);
};
//更新圈舍
export const updateHouseAndHurdle = () => {
  //更新月龄的前端超时时间是120000，不能决定是否成功
  return http.post(PORT1 + `/basicinfo/updateHouseAndHurdle`);
};

// 获取圈舍信息
export const initHouseAndHurdle = () => {
  return http.post<any>(PORT1 + `/basicinfo/initHouseAndHurdle`);
};

// 获取原产地信息
export const initManu = () => {
  return http.post<any>(PORT1 + `/basicinfo/initManu`);
};

// 分区调整
export const grassTransfer = params => {
  return http.post(PORT1 + `/basicinfo/grassTransfer`, params);
};
// 添加记录重复字段验证(编号)
export const validateGrassNum = params => {
  return http.post(PORT1 + `/basicinfo/validateGrassNum`, params);
};
// 删除记录
// export const deleteGrass = params => {
//   return http.post(PORT1 + `/user/delete`, params);
// };

// 切换记录状态
// export const changeUserStatus = params => {
//   return http.post(PORT1 + `/user/change`, params);
// };

// 重置记录密码
// export const resetUserPassWord = params => {
//   return http.post(PORT1 + `/user/rest_password`, params);
// };

// 获取树形用户列表
// export const getUserTreeList = params => {
//   return http.post(PORT1 + `/user/tree/list`, params);
// };

// // 获取用户状态字典
// export const getUserStatus = () => {
//   return http.get(PORT1 + `/user/status`);
// };

// // 获取用户性别字典
// export const getUserGender = () => {
//   return http.get(PORT1 + `/user/gender`);
// };

// // 获取用户部门列表
// export const getUserDepartment = () => {
//   return http.get(PORT1 + `/user/department`, {}, { cancel: false });
// };

// // 获取用户角色字典
// export const getUserRole = () => {
//   return http.get(PORT1 + `/user/role`);
// };
//更新关联信息
export const updateGrandparents = () => {
  return http.post(PORT1 + `/basicinfo/update_grandparents`);
};
