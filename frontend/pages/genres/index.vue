<template>
    <div class="genres-page-container">
        <GenresList :genres="genres" />
        <div
            class="load-more-button"
            @click="loadMoreGenres"
            v-if="showMoreButton"
        >
            Загрузить еще
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
const page = ref(0);
const genres = ref([]);
const showMoreButton = ref(true);
const { MAX_SELECT_GENRES_COUNT } = useRuntimeConfig().public;
const loadMoreGenres = async () => {
    page.value++;
    const new_genres = await Service.getGenresApiV1GenresGet(page.value);
    if (
        new_genres.length === 0 ||
        (page.value === 1 && new_genres.length < MAX_SELECT_GENRES_COUNT)
    ) {
        showMoreButton.value = false;
    }
    genres.value = [...genres.value, ...new_genres];
};
loadMoreGenres();
</script>
<style scoped lang="scss">
.genres-page-container {
    display: flex;
    flex-direction: column;

    gap: 20px;

    .load-more-button {
        cursor: pointer;
        color: $primary-text;
        font-weight: 500;
    }
}
</style>
