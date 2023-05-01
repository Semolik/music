<template>
    <Tracks :on-next-page="getPage" :page_size="MUSICIAN_ALL_TRACKS_LIMIT" />
</template>
<script setup>
import { Service } from "~/client";
const { MUSICIAN_ALL_TRACKS_LIMIT } = useRuntimeConfig().public;
const route = useRoute();
const { id } = route.params;

const getPage = async (page) => {
    return await Service.getMusicianPopularTracksApiV1MusicianProfileIdPopularGet(
        id,
        page.value
    );
};

definePageMeta({
    getTitle: true,
});
</script>
