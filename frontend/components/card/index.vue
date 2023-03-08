<template>
    <div class="card">
        <CardPicture
            :picture="picture"
            :icon="icon"
            :borderRadius="borderRadius"
            @click="$emit('picture-click')"
        />
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
        required: false,
        default: "5px",
    },
});
</script>
<style lang="scss">
.card {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    gap: 5px;
    cursor: pointer;
}
</style>
