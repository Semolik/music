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
const { grid, cut, rows } = defineProps({
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
    rows: {
        type: Number,
        default: 2,
    },
});

const tracksContainer = ref(null);
const rowElementsCount = ref(1);
onMounted(() => {
    window.addEventListener("resize", () => {
        if (!tracksContainer.value) return;
        const containerWidth = tracksContainer.value.clientWidth;
        const elementWidth = tracksContainer.value.children[0].clientWidth;
        const elementsCount = Math.floor(containerWidth / elementWidth);
        rowElementsCount.value = elementsCount > 6 ? elementsCount : 6;
    });
});
onBeforeUnmount(() => {
    window.removeEventListener("resize", () => {});
});

const cutElementsCount = computed(() => {
    if (!cut) return 0;
    return rows * rowElementsCount.value;
});
watch(cutElementsCount, (value) => {
    if (!tracksContainer.value) return;
    const elements = tracksContainer.value.children;
    for (let i = 0; i < elements.length; i++) {
        if (i >= value) {
            elements[i].style = "display: none";
        } else {
            elements[i].style = "";
        }
    }
});
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
