<template>
  <div class="login-container">
    <div class="login-card">
      <!-- 左侧面板 -->
      <div class="login-left">
        <div class="particles">
          <span v-for="i in 8" :key="i" class="particle"></span>
        </div>
        <div class="left-content">
          <h1 class="left-title">草地作物病虫害<br />智能监测系统</h1>
          <p class="left-subtitle">AgroGuard Meadow Guard</p>
          <p class="left-desc">草地作物全生命周期<br />病虫害监测、预警与防治管理平台</p>
        </div>
      </div>

      <!-- 右侧面板 -->
      <div class="login-right">
        <SwitchDark class="dark-switch" />
        <div class="login-form">
          <div class="login-logo">
            <h2 class="logo-text">系统登录</h2>
            <p class="logo-sub">欢迎回来，请输入您的账号</p>
          </div>
          <LoginForm />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" name="login">
import LoginForm from "./components/LoginForm.vue";
import SwitchDark from "@/components/SwitchDark/index.vue";
</script>

<style scoped lang="scss">
@import "./index";
</style>
