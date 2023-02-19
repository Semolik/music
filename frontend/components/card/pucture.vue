<template>
    <div class="card-picture">
        <img :src="picture" v-if="picture" />
        <Icon name="material-symbols:person-rounded" v-else />
    </div>
</template>
<script setup>
const { picture, icon } = defineProps({
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
.card-picture {
    @include flex-center;
    width: 100%;

    background-color: $quaternary-bg;
    border-radius: 10px;
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
