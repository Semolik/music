<template>
    <div class="genres-page-container">
        <GenresList :genres="genres" />
        <AppButton @click="loadMoreGenres" v-if="showMoreButton" active>
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
useHead({
    title: "Жанры",
});
definePageMeta({
    title: "Жанры",
});
import { Service } from "@/client";
const page = ref(0);
const genres = ref([]);
const showMoreButton = ref(false);
const { GENRES_ALL_LIMIT } = useRuntimeConfig().public;
const loadMoreGenres = async () => {
    page.value++;
    const new_genres = await Service.getGenresApiV1GenresGet(page.value);
    showMoreButton.value = new_genres.length === GENRES_ALL_LIMIT;
    genres.value = [...genres.value, ...new_genres];
};
loadMoreGenres();
</script>
<style scoped lang="scss">
.genres-page-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>
