<template>
    <Selection
        title="Жанры"
        description="Выберите любимый жанр и начните слушать музыку"
    >
        <div class="genres-container">
            <GenresCard
                v-for="genre in genres"
                :key="genre.id"
                :genre="genre"
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
    height: 100%;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    padding-bottom: 20px;
}
</style>
