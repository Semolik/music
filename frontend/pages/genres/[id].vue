<template>
    <NuxtPage />
</template>
<script setup>
import { Service } from "~/client";
import { routesNames } from "@typed-router";
import { useHeaderStore } from "~/stores/header";
const headerStore = useHeaderStore();
const { setTitle } = headerStore;
const route = useRoute();
const { id } = route.params;
const genre = ref(null);
const getGenreName = async () => {
    if (genre.value) return genre.value.name;
    genre.value = await Service.getGenreInfoApiV1GenresGenreIdInfoGet(id);
    return genre.value.name;
};

watch(
    () => route.name,
    async (value) => {
        headerStore.reset();
        headerStore.currentRouteName = route.name;
        switch (value) {
            case routesNames.genresId.index:
                headerStore.title = null;
                break;
            case routesNames.genresId.idTracks:
                setTitle(`Популярные треки жанра ${await getGenreName()}`);
                break;
            case routesNames.genresId.idAlbums:
                setTitle(`Популярные альбомы жанра ${await getGenreName()}`);
                break;
            case routesNames.genresId.idMusicians:
                setTitle(`Популярные музыканты жанра ${await getGenreName()}`);
                break;
            case routesNames.genresId.idNewAlbums:
                setTitle(`Новые альбомы жанра ${await getGenreName()}`);
                break;
        }
    },
    { immediate: true }
);
</script>
