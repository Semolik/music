<template>
    <div class="index-page">
        <Slider />
        <Genres />
        <Chart />
    </div>
</template>
<script setup>
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
