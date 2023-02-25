<template>
    <div @click="login" class="login">Авторизоваться</div>
    <div @click="logout" class="login">Выйти</div>
    <div class="login">{{ logined }}</div>
</template>
<script setup>
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const login = () => {
    authStore.loginRequest("admin", "abobus123");
};
const logout = () => {
    authStore.logoutRequest();
};
</script>

<style lang="scss">
.login {
    color: $primary-text;
}
</style>
