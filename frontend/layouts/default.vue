<template>
    <NuxtErrorBoundary @error="handleError">
        <div class="default-layout">
            <AppAside v-if="$viewport.isGreaterOrEquals('lg')" />
            <div
                :class="[
                    'content-container',
                    { 'player-active': currentTrack },
                ]"
            >
                <AppHeader />
                <div
                    :class="[
                        'app-content',
                        { 'enable-padding': !disableDefaultLayoutPadding },
                    ]"
                >
                    <slot />
                </div>
                <AppPlayer />
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
        position: relative;

        @include lg(true) {
            padding-bottom: 70px;

            &.player-active {
                padding-bottom: 200px;
            }
        }
        &.player-active {
            padding-bottom: 125px;
        }

        .app-content {
            flex-grow: 1;
            overflow-y: scroll;

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
import { usePlayerStore } from "~/stores/player";
import { storeToRefs } from "pinia";
const { currentTrack } = storeToRefs(usePlayerStore());
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
