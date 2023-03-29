<template>
    <Selection
        title="Жанры"
        description="Выберите любимый жанр и начните слушать музыку"
        leftText="Все жанры"
        leftTextLinkName="genres"
    >
        <div class="genres-container">
            <GenresCard
                v-for="genre in genres"
                :key="genre.id"
                :genre="genre"
                class="genre-card"
                min
            />
        </div>
    </Selection>
</template>
<script setup>
import { Service } from "~~/client";
const { all } = defineProps({
    all: {
        type: Boolean,
        required: false,
        default: true,
    },
});
const genres = await Service.getGenresApiV1GenresGet();
</script>
<style lang="scss" scoped>
.genres-container {
    display: grid;
    --size: 200px;
    @include sm(true) {
        --size: 160px;
    }
    grid-template-columns: repeat(auto-fill, minmax(var(--size), 1fr));
    gap: 10px;
}
</style>
