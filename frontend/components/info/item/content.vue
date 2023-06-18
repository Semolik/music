<template>
    <div class="title">{{ item.title }}</div>
    <div :class="['value', { left: item.left }]">{{ item.value }}</div>
    <div class="go-to" v-if="item.to">
        <span>Перейти</span>
        <Icon :name="IconsNames.forwardIcon" />
    </div>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
const { item } = defineProps({
    item: Object,
});
</script>
<style lang="scss" scoped>
.title,
.value {
    padding: 10px;
}

.title {
    font-size: 16px;
    background-color: $quaternary-bg-2;
    color: $secondary-text;
    @include flex-center;
}
.value {
    font-size: 16px;
    color: $primary-text;
    background-color: $quinary-bg;
    word-break: break-word;

    &:not(.left) {
        @include flex-center;
    }
}
.go-to {
    @include flex-center;
    background-color: $quaternary-bg;
    color: $secondary-text;
    cursor: pointer;
    grid-column: 1 / 3;
    grid-row: 2;
    padding: 10px;
    gap: 10px;

    svg {
        width: 20px;
        height: 20px;
        color: $secondary-text;
    }
}
</style>
