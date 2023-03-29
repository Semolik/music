<template>
    <nuxt-link
        class="genre-card"
        :to="{
            name: routesNames.genresId,
            params: {
                id: genre.id,
            },
        }"
    >
        <img class="genre-card__image" :src="genre.picture" :alt="genre.name" />

        <div class="genre-card__name">
            {{ genre.name }}
        </div>
    </nuxt-link>
</template>
<script setup>
import { routesNames } from "@typed-router";
const { genre } = defineProps({
    genre: {
        type: Object,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.genre-card {
    display: flex;
    position: relative;
    gap: 10px;
    width: 100%;
    height: 100%;
    text-decoration: none;
    aspect-ratio: 3;
    color: $primary-text;
    transition: 0.2s;
    isolation: isolate;
    border-radius: 5px;
    overflow: hidden;
    &:hover {
        box-shadow: 0px 0px 20px 10px rgba(77 117 54 / 60%);
    }
    &__image {
        position: absolute;
        inset: 0;
        border-radius: 5px;
        width: 100%;
        height: 100%;

        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.5) blur(5px);
        z-index: -1;
    }
    &__name {
        @include flex-center;
        width: 100%;
        z-index: 1;
        padding: 10px;
        font-size: 16px;
        font-weight: 500;
        text-align: center;
    }
}
</style>
