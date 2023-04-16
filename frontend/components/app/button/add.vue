<template>
    <div class="add" v-if="!to">
        <Icon :name="IconsNames.plusIcon" />
    </div>
    <nuxt-link v-else class="add" :to="to">
        <Icon :name="IconsNames.plusIcon" />
    </nuxt-link>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { to } = defineProps({
    to: {
        type: Object,
        default: null,
    },
});
</script>
<style lang="scss" scoped>
.add {
    border: 1px solid $quaternary-text;
    width: 40px;
    border-radius: 5px;
    @include flex-center;
    background-color: $secondary-bg;

    &:hover {
        border-color: $tertiary-text;
    }
}
</style>
