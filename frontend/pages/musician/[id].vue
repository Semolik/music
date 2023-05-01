<template>
    <NuxtPage />
</template>
<script setup>
import { useHeaderStore } from "~/stores/header";
import { routesNames } from "@typed-router";
import { Service } from "~/client";
const headerStore = useHeaderStore();
const { setTitle } = headerStore;
const route = useRoute();
const { id } = route.params;
const musician = ref(null);
const getMusicianName = async () => {
    if (musician.value) return musician.value.name;
    musician.value =
        await Service.getPublicProfileInfoApiV1MusicianProfileIdGet(id);
    return musician.value.name;
};

watch(
    () => route.name,
    async (value) => {
        headerStore.reset();
        headerStore.currentRouteName = value;
        switch (value) {
            case routesNames.musicianId.index:
                headerStore.title = null;
                break;
            case routesNames.musicianId.idTracks:
                setTitle(
                    `Популярные треки музыканта ${await getMusicianName()}`
                );
                break;
            case routesNames.musicianId.idAlbums:
                setTitle(
                    `Популярные альбомы музыканта ${await getMusicianName()}`
                );
                break;
            case routesNames.musicianId.idClips:
                setTitle(`Клипы музыканта ${await getMusicianName()}`);
                break;
        }
    },
    { immediate: true }
);
</script>
