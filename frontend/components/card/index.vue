<template>
    <div class="card">
        <CardPucture :picture="picture" :icon="icon" />
        <div class="card-text">{{ text }}</div>
    </div>
</template>
<script setup>
const { text } = defineProps({
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
});
</script>
<style lang="scss">
.card {
    @include flex-center;
    flex-direction: column;
    height: 100%;
    width: 100%;
    gap: 5px;
}
</style>
