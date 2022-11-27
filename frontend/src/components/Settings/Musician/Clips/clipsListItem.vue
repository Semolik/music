<template>
    <component :is="baseUrl ? 'router-link' : 'div'" :[baseUrl&&`to`]="`${baseUrl}${clip.id}`"
        @click="$emit('clip-click', clip)" class="clip-item" :key="clip.id">
        <div class="picture-container">
            <img :src="clip.picture" :alt="clip.name">
        </div>
        <div class="name">{{ clip.name }}</div>
    </component>
</template>
<script>
export default {
    props: {
        baseUrl: String,
        clip: Object,
    }
}
</script>
<style lang="scss">
.clip-item {
    display: flex;
    flex-direction: column;
    gap: 5px;
    cursor: pointer;
    color: var(--color-text);
    text-decoration: none;

    .picture-container {
        position: relative;
        display: flex;
        aspect-ratio: 16 / 9;
        overflow: hidden;
        border-radius: 10px;

        img {
            object-fit: cover;
            width: 100%;
            height: 100%;
        }

        &::after {
            content: '';
            background-color: rgba($color: white, $alpha: 0.15);
            position: absolute;
            inset: 0;
            opacity: 0;
            transition: opacity .2s;
        }
    }

    &:hover .picture-container::after {
        opacity: 1;
    }

    .name {
        font-size: 18px;
        text-align: center;
        word-wrap: break-all;

    }
}
</style>