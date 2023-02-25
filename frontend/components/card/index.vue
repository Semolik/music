<template>
    <div class="card">
        <CardPicture
            :picture="picture"
            :icon="icon"
            :borderRadius="borderRadius"
        />
        <div class="card-text">{{ text }}</div>
    </div>
</template>
<script setup>
const { text, picture, icon, borderRadius } = defineProps({
    text: {
        type: String,
        required: true,
    },
    picture: {
        type: [String, null],
        required: true,
    },
    icon: {
        type: String,
        required: true,
    },
    borderRadius: {
        type: Number,
        required: false,
        default: 4,
    },
});
</script>
<style lang="scss">
.card {
    @include flex-center;
    flex-direction: column;
    height: 100%;
    width: 100%;
    gap: 5px;
    cursor: pointer;
}
</style>
