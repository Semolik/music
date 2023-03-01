<template>
    <NuxtLink :to="to" class="menu-card">
        <Icon :name="icon" />
        <span>{{ text }}</span>
    </NuxtLink>
</template>
<script setup>
const { to, icon, text } = defineProps({
    to: {
        type: Object,
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    text: {
        type: String,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.menu-card {
    color: $secondary-text;
    @include flex-center;
    flex-direction: column;
    gap: 10px;
    background-color: $secondary-bg;
    padding: 15px;
    border-radius: 10px;
    svg {
        width: 50px;
        height: 50px;
    }
}
</style>
