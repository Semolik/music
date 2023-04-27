<template>
    <div class="index-page">
        <Slider />
        <Genres />
        <Chart />
        <History v-if="logined" />
        <NewReleases />
    </div>
</template>
<script setup>
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
useHead({
    title: "Главная",
});
</script>
<style lang="scss" scoped>
.index-page {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>
