<template>
    <client-only>
        <div class="loading-container" v-auto-animate>
            <Icon :name="IconsNames.playIcon" v-if="paused" />
            <div class="dot" v-else></div>
        </div>
    </client-only>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
const { paused } = defineProps({
    paused: Boolean,
});
</script>
<style lang="scss" scoped>
.loading-container {
    @include flex-center;
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1;
    svg {
        color: $accent;
        width: 25px;
        height: 25px;
    }

    @keyframes bounce {
        0% {
            scale: 1;
        }
        50% {
            scale: 1.5;
        }
        100% {
            scale: 1;
        }
    }

    .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: $accent;
        margin: 0 5px;
        animation: bounce 0.7s infinite;
    }
}
</style>
