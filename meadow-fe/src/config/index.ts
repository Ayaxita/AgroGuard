// ? 全局默认配置项

// 首页地址（默认）
export const HOME_URL: string = "/home/index";

// 登录页地址（默认）
export const LOGIN_URL: string = "/login";

// 默认主题颜色
export const DEFAULT_PRIMARY: string = "#009688";

// 路由白名单地址（本地存在的路由 staticRouter.ts 中）
// staticRouter.ts 中已经包含了"/basic/basicinfo/detail"这个路径，但是不知道为什么没有起作用，所以在这个位置在加了一便
export const ROUTER_WHITE_LIST: string[] = ["/500", "/basic/basicinfo/detail", "/basic/basicinfo/qrcode"];

// 高德地图 key
export const AMAP_MAP_KEY: string = "";

// 百度地图 key
export const BAIDU_MAP_KEY: string = "";
