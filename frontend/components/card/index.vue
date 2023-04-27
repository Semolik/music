<template>
    <div :class="['card', { 'is-link': isLink }]">
        <CardPicture
            :picture="picture"
            :icon="icon"
            :borderRadius="borderRadius"
            @click="$emit('picture-click')"
        >
            <slot name="picture" />
        </CardPicture>
        <slot />
    </div>
</template>
<script setup>
const { picture, icon, borderRadius, isLink } = defineProps({
    picture: {
        type: [String, null],
        required: true,
    },
    icon: {
        type: String,
    },
    borderRadius: {
        type: String,
        required: false,
        default: "5px",
    },
    isLink: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss" scoped>
.card {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    gap: 5px;
    cursor: pointer;
    &.is-link {
        background-color: $secondary-bg;
        padding: 10px;
        border-radius: 10px;
        @include lg {
            &:hover {
                background-color: $secondary-bg-2;
            }
        }
    }
}
</style>
