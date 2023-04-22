<template>
    <nuxt-link class="genre-min-card" v-if="min" :to="link">
        <div class="genre-card__name">
            {{ genre.name }}
        </div>
        <img :src="genre.picture" />
    </nuxt-link>
    <card
        v-else
        :picture="genre.picture"
        borderRadius="5px"
        @picture-click="() => $router.push(link)"
    >
        <div class="genre-card__name">
            {{ genre.name }}
        </div>
    </card>
</template>
<script setup>
import { routesNames } from "@typed-router";
const { genre } = defineProps({
    genre: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        required: false,
        default: false,
    },
});

const link = computed(() => ({
    name: routesNames.genresId,
    params: { id: genre.id },
}));
</script>
<style lang="scss" scoped>
.genre-card__name {
    font-weight: 500;
    color: $secondary-text;
    text-align: center;
    word-break: break-all;
    padding: 0px 10px;
}
.genre-min-card {
    cursor: pointer;
    position: relative;
    height: min-content;
    aspect-ratio: 2;
    width: 100%;
    isolation: isolate;
    border-radius: 5px;
    overflow: hidden;
    background-color: $tertiary-bg;
    --brightness: 0.5;
    &:hover {
        --brightness: 0.7;
    }
    img {
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: -1;
        transition: filter 0.2s ease-in-out;
        filter: brightness(var(--brightness)) blur(2px);
    }

    .genre-card__name {
        @include flex-center;
        color: $primary-text;
        height: 100%;
    }
}
</style>
