<template>
    <header :class="{ 'header-bar-active': headerBarActive }">
        <AppHeaderSearch v-model:searchActive="searchIsActive" />
        <div
            class="header-bar"
            v-if="headerBarActive && (links.length || currentPageTitle)"
        >
            <div class="current-page-title" v-if="currentPageTitle">
                {{ currentPageTitle }}
            </div>
            <ClientOnly>
                <div class="links" v-if="links.length">
                    <nuxt-link
                        v-for="link in links"
                        :key="link.name"
                        :to="{ name: link.name }"
                        class="header-bar-link"
                    >
                        {{ link.title }}
                    </nuxt-link>
                </div>
            </ClientOnly>
        </div>
    </header>
</template>
<script setup>
import { useEventBus } from "@vueuse/core";
const openSearchBus = useEventBus("openSearch");
const viewport = useViewport();
const router = useRouter();
const links = computed(() => router.currentRoute.value.meta.headerLinks || []);
const headerBarActive = ref(false);
watch(
    [viewport.breakpoint, router.currentRoute],
    ([breakpoint, route]) => {
        headerBarActive.value =
            viewport.isLessThan("lg") || route.name !== "index";
    },
    { immediate: true }
);
const searchIsActive = ref(false);
const currentPageTitle = ref(null);
const unsubscribeOpenSearchBus = openSearchBus.on(() => {
    searchIsActive.value = true;
});

onBeforeUnmount(() => {
    unsubscribeOpenSearchBus();
});
useHead({
    title: currentPageTitle,
});
watch(
    router.currentRoute,
    (value) => {
        if (value.meta?.getTitle) {
            onMounted(async () => {
                currentPageTitle.value = document.title;
            });
        } else {
            currentPageTitle.value = value.meta?.title;
        }
    },
    { immediate: true }
);

onMounted(() => {
    window.addEventListener("keydown", (event) => {
        if (event.ctrlKey && event.key === "k") {
            event.preventDefault();
            searchIsActive.value = !searchIsActive.value;
        }
        if (event.key === "Escape" && searchIsActive.value) {
            searchIsActive.value = false;
        }
    });
});

onUnmounted(() => {
    window.removeEventListener("keydown", () => {});
});
</script>
<style lang="scss" scoped>
header {
    padding: 20px;
    padding-bottom: 0px;

    display: none;
    &.header-bar-active {
        padding: 0px;
        display: flex;
    }
    .header-bar {
        color: $primary-text;
        width: 100%;
        padding: 20px;
        padding-bottom: 0px;
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 20px;
        @include lg(true) {
            flex-direction: column;
            padding: 10px;
            padding-bottom: 0;
        }
        .current-page-title {
            font-size: 1.5rem;
            font-weight: 500;
            color: $secondary-text;
            @include lg(true) {
                text-align: center;
                width: 100%;
                padding-top: 5px;
            }
        }
        .links {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            @include lg(true) {
                width: 100%;
            }
            .header-bar-link {
                font-weight: 500;
                color: $secondary-text;
                border: 1px solid $tertiary-text;
                padding: 5px 20px;
                border-radius: 10px;
                @include flex-center;
                @include lg(true) {
                    flex-grow: 1;
                }
                @include lg {
                    &:not(.router-link-active):hover {
                        border-color: $accent;
                        color: $accent;
                    }
                }
                &.router-link-active {
                    border-color: $accent;
                    background-color: $accent;
                    color: $primary-bg;
                }
            }
        }
    }

    .search-button {
        @include flex-center;
        flex-grow: 1;
        gap: 10px;
        padding: 10px;
        border-radius: 10px;
        color: $secondary-text;
        height: min-content;
        cursor: pointer;
        background-color: $tertiary-bg;
        &:hover {
            background-color: $quaternary-bg;
        }

        svg {
            width: 20px;
            height: 20px;
        }
        .button-text {
            flex-grow: 1;
        }
        .button-hotkey-text {
            border-radius: 5px;
            color: $secondary-text;
            border: 1px solid $secondary-text;
            padding: 3px 5px;
            user-select: none;
        }
    }
}
</style>
