<template>
    <div class="favorite-tracks-container">
        <TrackCard
            v-for="(track, index) in tracks"
            :key="track.id"
            v-model:track="tracks[index]"
        />
    </div>
    <NotFound v-if="!tracks.length" />
</template>
<script setup>
import { Service } from "@/client";
const { FAVORITE_TRACKS_LIMIT } = useRuntimeConfig().public;
const tracks = ref([]);
const page = ref(0);
const loadMoreButton = ref(false);
const loadMore = async () => {
    page.value++;
    const new_tracks = await Service.getLikedTracksApiV1TracksLikedGet(
        page.value
    );
    tracks.value = tracks.value.concat(new_tracks);
    loadMoreButton.value = new_tracks.length == FAVORITE_TRACKS_LIMIT;
};
loadMore();
</script>
<style lang="scss" scoped>
.favorite-tracks-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
