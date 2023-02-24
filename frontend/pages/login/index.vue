<template>
    <div @click="login" class="login">Авторизоваться</div>
    <div @click="logout" class="login">Выйти</div>
</template>
<script setup>
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
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
