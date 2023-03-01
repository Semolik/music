<template>
    <div :class="['card-picture', { min: min }]">
        <img :src="picture" v-if="picture" />
        <Icon :name="icon" v-else />
        <slot />
    </div>
</template>
<script setup>
const { picture, icon, borderRadius } = defineProps({
    picture: {
        type: [String, null],
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    borderRadius: {
        type: String,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss">
.card-picture {
    position: relative;
    @include flex-center;
    aspect-ratio: 1;
    &.min {
        height: 100%;
        background-color: $tertiary-bg;
    }
    &:not(.min) {
        width: 100%;
        background-color: $quaternary-bg;
    }
    border-radius: v-bind(borderRadius);
    overflow: hidden;
    aspect-ratio: 1;
    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    svg {
        padding: 20%;
        height: 100%;
        width: 100%;
        color: $secondary-text;
    }
}
</style>
