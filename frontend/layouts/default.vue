<template>
    <NuxtErrorBoundary>
        <div class="default-layout">
            <AppAside v-if="$viewport.isGreaterOrEquals('lg')" />
            <div class="content-container">
                <AppHeader v-if="$viewport.isGreaterOrEquals('lg')" />
                <div class="app-content">
                    <slot />
                </div>
            </div>
            <AppBottomBar v-if="$viewport.isLessThan('lg')" />
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
    @include lg(true) {
        grid-template-columns: 1fr;
        grid-template-rows: 1fr;
    }

    .content-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        .app-content {
            flex-grow: 1;
            overflow: auto;
            padding: 0px 20px;
            height: 100%;
        }
    }
}
</style>
<script setup>
const fixIssue = (error) => {
    error.value = null;
};
</script>
