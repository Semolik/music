<template>
    <NuxtLink :to="to" class="menu-card" v-if="to">
        <Icon :name="icon" />
        <span>{{ text }}</span>
    </NuxtLink>
    <div class="menu-card" v-else @click="onClick">
        <Icon :name="icon" />
        <span>{{ text }}</span>
    </div>
</template>
<script setup>
const { to, icon, text, onClick } = defineProps({
    to: {
        type: Object,
        required: false,
    },
    icon: {
        type: String,
        required: true,
    },
    text: {
        type: String,
        required: true,
    },
    onClick: {
        type: Function,
        required: false,
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
