<template>
    <NuxtErrorBoundary @error="handleError">
        <div class="full-page-layout">
            <slot />
        </div>
        <template #error="{ error }">
            <AppError :error="error" @clearError="fixIssue(error)" />
        </template>
    </NuxtErrorBoundary>
</template>
<style lang="scss">
.full-page-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
    .app-content {
        flex-grow: 1;
        overflow: auto;
        padding-inline: 20px;
        @include lg(true) {
            padding-inline: 10px;
        }
        height: 100%;
    }
}
</style>
<script setup>
const fixIssue = (error) => {
    error.value = null;
};
const handleError = (error) => {
    console.error(error);
};
</script>
