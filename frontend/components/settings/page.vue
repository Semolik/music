<template>
    <div class="page-container">
        <div class="page-container-title">
            <span>{{ title }}</span>
        </div>
        <div class="page-container-content">
            <slot />
        </div>
    </div>
</template>
<script setup>
const { title, maxWidth, padding } = defineProps({
    title: {
        type: String,
        required: true,
    },
    maxWidth: {
        type: String,
        default: "400px",
    },
    padding: {
        type: String,
        default: "2rem",
    },
});
</script>
<style lang="scss" scoped>
.page-container {
    @include flex-center;
    flex-direction: column;
    @include sm {
        padding: v-bind(padding);
    }
    .page-container-title {
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 20px;
        color: $secondary-text;
        text-align: center;
        @include flex-center;
    }
    .page-container-content {
        max-width: v-bind(maxWidth);
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: 10px;
    }
}
</style>
