<template>
    <Tracks :on-next-page="loadMore" :page_size="POPULAR_TRACKS_LIMIT_ALL" />
</template>
<script setup>
import { Service } from "~/client";
const { POPULAR_TRACKS_LIMIT_ALL } = useRuntimeConfig().public;
const route = useRoute();
const { id } = route.params;
const genre = await Service.getGenreInfoApiV1GenresGenreIdInfoGet(id);
const loadMore = async (page) => {
    return await Service.getPopularTracksByGenreIdApiV1GenresGenreIdTracksGet(
        id,
        page.value
    );
};
useHead({
    title: "Популярные треки жанра " + genre.name,
});
definePageMeta({
    getTitle: true,
});
</script>
