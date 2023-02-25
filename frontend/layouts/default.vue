<template>
    <NuxtErrorBoundary>
        <div class="default-layout">
            <AppAside />
            <div class="content-container">
                <AppHeader />
                <div class="app-content">
                    <slot />
                </div>
            </div>
        </div>
        <template #error="{ error }">
            <AppError :error="error" @clearError="fixIssue(error)" />
        </template>
    </NuxtErrorBoundary>
</template>
<style lang="scss">
.default-layout {
    display: grid;
    grid-template-columns: min-content 1fr;
    height: 100%;
    .content-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        .app-content {
            flex-grow: 1;
            overflow: auto;
            padding: 0px 20px;
        }
    }
}
</style>
<script setup>
const fixIssue = (error) => {
    error.value = null;
};
</script>
