<template>
    <NuxtErrorBoundary @error="handleError">
        <div class="default-layout">
            <AppAside v-if="$viewport.isGreaterOrEquals('lg')" />
            <div class="content-container">
                <AppHeader />
                <div
                    :class="[
                        'app-content',
                        { 'enable-padding': !disableDefaultLayoutPadding },
                    ]"
                >
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
        overflow-x: hidden;

        @include lg(true) {
            padding-bottom: 70px;
        }
        .app-content {
            flex-grow: 1;
            // overflow: scroll;

            &.enable-padding {
                padding: 20px;
                @include lg(true) {
                    padding: 10px;
                }
            }
        }
    }
}
</style>
<script setup>
const router = useRouter();
const disableDefaultLayoutPadding = computed(
    () => router.currentRoute.value.meta.disableDefaultLayoutPadding
);
const fixIssue = (error) => {
    error.value = null;
};
const handleError = (error) => {
    console.error(error);
};
</script>
