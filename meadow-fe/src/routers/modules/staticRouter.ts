import { RouteRecordRaw } from "vue-router";
import { HOME_URL, LOGIN_URL } from "@/config";

/**
 * staticRouter (静态路由)
 */
export const staticRouter: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: HOME_URL
  },
  {
    path: LOGIN_URL,
    name: "login",
    component: () => import("@/views/login/index.vue"),
    meta: {
      title: "登录"
    }
  },
  {
    path: "/layout",
    name: "layout",
    component: () => import("@/layouts/index.vue"),
    // component: () => import("@/layouts/indexAsync.vue"),
    redirect: HOME_URL,
    children: []
  },
  {
    path: "/supply/v_suppliersinfo/select_page",
    name: "v_suppliersinfo_select_page",
    component: () => import("@/views/supply/v_suppliersinfo/select_page/index.vue")
  },
  {
    path: "/supply/f_suppliersinfo/select_page",
    name: "f_suppliersinfo_select_page",
    component: () => import("@/views/supply/f_suppliersinfo/select_page/index.vue")
  },
  {
    path: "/basic/basicinfo/detail",
    name: "basicinfo_detail",
    component: () => import("@/views/basic/basicinfo/detail/index.vue")
  },
  {
    path: "/basic/basicinfo/qrcode",
    name: "basicinfo_qrcode",
    component: () => import("@/views/basic/basicinfo/qrcode/index.vue")
  },
  {
    path: "/statistic/xipu/detail",
    name: "xipu_detail",
    component: () => import("@/views/basic/basicinfo/detail/index.vue")
  },
  {
    path: "/test",
    name: "ChatboxTest",
    component: () => import("@/components/ChatBox/ChatBubble.vue")
  }
];

/**
 * errorRouter (错误页面路由)
 */
export const errorRouter = [
  {
    path: "/403",
    name: "403",
    component: () => import("@/components/ErrorMessage/403.vue"),
    meta: {
      title: "403页面"
    }
  },
  {
    path: "/404",
    name: "404",
    component: () => import("@/components/ErrorMessage/404.vue"),
    meta: {
      title: "404页面"
    }
  },
  {
    path: "/500",
    name: "500",
    component: () => import("@/components/ErrorMessage/500.vue"),
    meta: {
      title: "500页面"
    }
  },
  // Resolve refresh page, route warnings
  {
    path: "/:pathMatch(.*)*",
    component: () => import("@/components/ErrorMessage/404.vue")
  }
];
