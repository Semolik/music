<template>
    <div class="musician-avatar">
        <img :src="avatar" v-if="avatar" />
        <Icon name="material-symbols:person-rounded" v-else />
    </div>
</template>
<script setup>
const { avatar } = defineProps({
    avatar: {
        type: [String, null],
        required: true,
    },
});
</script>
<style lang="scss">
.musician-avatar {
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
