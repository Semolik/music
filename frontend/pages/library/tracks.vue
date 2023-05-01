<template>
    <Tracks :on-next-page="loadMore" :page_size="FAVORITE_TRACKS_LIMIT" />
</template>
<script setup>
import { Service } from "@/client";
const { FAVORITE_TRACKS_LIMIT } = useRuntimeConfig().public;
const loadMore = async (page) => {
    return await Service.getLikedTracksApiV1TracksLikedGet(page.value);
};
</script>
