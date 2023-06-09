<template>
    <ClientOnly v-if="animate">
        <div v-auto-animate :class="['tracks', { grid }]" ref="tracksContainer">
            <slot />
        </div>
    </ClientOnly>
    <div :class="['tracks', { grid }]" v-else ref="tracksContainer">
        <slot />
    </div>
</template>
<script setup>
const { grid, cut } = defineProps({
    grid: {
        type: Boolean,
        default: false,
    },
    cut: {
        type: Boolean,
        default: false,
    },
    animate: {
        type: Boolean,
        default: false,
    },
});

const tracksContainer = ref(null);
const rowElementsCount = ref(1);
const setRowElementsCount = () => {
    if (!tracksContainer.value) return;
    const containerWidth = tracksContainer.value.clientWidth;
    if (!tracksContainer.value.children[0]) return;
    const elementWidth = tracksContainer.value.children[0].clientWidth;
    const elementsCount = Math.floor(containerWidth / elementWidth);
    rowElementsCount.value = elementsCount;
};
if (cut) {
    onMounted(() => {
        watch(
            rowElementsCount,
            (value) => {
                const elements = tracksContainer.value.children;

                const cut_els = (value === 1 ? 6 : 3) * value;
                for (let i = 0; i < elements.length; i++) {
                    if (i >= cut_els) {
                        elements[i].style.display = "none";
                    }
                }
            },
            { immediate: true }
        );
        setRowElementsCount();
        window.addEventListener("resize", () => {
            setRowElementsCount();
        });
    });
    onBeforeUnmount(() => {
        window.removeEventListener("resize", () => {});
    });
}
</script>
<style lang="scss" scoped>
.tracks {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    &.grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        grid-template-rows: min-content;
        height: min-content;
        @include lg(true) {
            grid-template-columns: 1fr;
        }

        & > * {
            flex-grow: 1;
        }
    }
}
</style>
