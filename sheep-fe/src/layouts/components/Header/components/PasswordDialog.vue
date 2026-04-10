<template>
  <el-dialog v-model="dialogVisible" title="修改密码" width="500px" draggable>
    <el-form
      ref="ruleFormRef"
      label-width="100px"
      label-suffix=" :"
      :rules="rules"
      :disabled="!dialogVisible"
      :model="drawerProps"
      :hide-required-asterisk="!dialogVisible"
    >
      <el-form-item label="旧密码" prop="password_old">
        <el-input
          v-model="drawerProps.password_old"
          type="password"
          show-password
          placeholder="请填写旧密码"
          clearable
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password_new">
        <el-input
          v-model="drawerProps.password_new"
          type="password"
          show-password
          placeholder="请填写新密码"
          clearable
        ></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="password_confirm">
        <el-input v-model="drawerProps.password_confirm" type="password" placeholder="请二次确认新密码" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <ul>
          <li>密码不能包含个人信息</li>
          <li>密码长度应该为6-20位</li>
          <li>密码不能全是数字</li>
        </ul>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="cancel(ruleFormRef)">取消</el-button>
        <el-button type="primary" @click="confirm(ruleFormRef)">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { resetUserPassword } from "@/api/modules/user";
import router from "@/routers";
import { useUserStore } from "@/stores/modules/user";
import { ElMessage } from "element-plus";
import { FormInstance } from "element-plus";
import md5 from "md5";
import { ref, watch } from "vue";

const userStore = useUserStore();
const dialogVisible = ref(false);
const openDialog = () => {
  dialogVisible.value = true;
};

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === "Enter") {
    confirm(ruleFormRef.value);
  }
};

watch(dialogVisible, () => {
  if (dialogVisible.value) {
    document.addEventListener("keydown", handleKeydown);
    // console.log("添加了");
  } else {
    document.removeEventListener("keydown", handleKeydown);
    // console.log("删除了");
  }
});

defineExpose({ openDialog });

const ruleFormRef = ref<FormInstance>();
const drawerProps = ref({
  password_old: "",
  password_new: "",
  password_confirm: ""
});
const checkConfirm = (rule: any, value: string, callback: any) => {
  if (value !== drawerProps.value.password_new) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};
const rules = {
  password_old: [
    { required: true, message: "请填写旧密码", trigger: "blur" },
    { min: 6, max: 20, message: "长度在 6 到 20 个字符", trigger: "blur" }
  ],
  password_new: [
    { required: true, message: "请填写新密码", trigger: "blur" },
    { min: 6, max: 20, message: "长度在 6 到 20 个字符", trigger: "blur" }
  ],
  password_confirm: [
    { required: true, message: "请二次确认新密码", trigger: "blur" },
    { min: 6, max: 20, message: "长度在 6 到 20 个字符", trigger: "blur" },
    { validator: checkConfirm, trigger: "blur" }
  ]
};

const cancel = (formEl: FormInstance | undefined) => {
  dialogVisible.value = false;
  formEl?.resetFields();
};

const confirm = (formEl: FormInstance | undefined) => {
  // console.log("触发修改密码");
  if (!formEl) return;
  formEl.validate(async valid => {
    if (valid) {
      // console.log("submit!");
      let params = {
        username: userStore.userInfo.name,
        password_old: md5(drawerProps.value.password_old),
        password_new: md5(drawerProps.value.password_new)
      };
      const res = await resetUserPassword(params);
      if (res.code === 200) {
        ElMessage.success(res.msg);
        dialogVisible.value = false;
        formEl?.resetFields();
        userStore.$reset();
        router.push("/login");
      } else {
        ElMessage.error(res.msg);
      }
    } else {
      // console.log("error submit!!");
    }
  });
};
</script>
<style scoped>
ul {
  padding: 0;
  margin: 0;
}
</style>
