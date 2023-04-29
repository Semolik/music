<template>
    <div class="favorite-tracks-container">
        <TrackCard
            v-for="(track, index) in tracks"
            :key="track.id"
            v-model:track="tracks[index]"
        />
    </div>
</template>
<script setup>
import { Service } from "@/client";
const tracks = ref(await Service.getLikedTracksApiV1TracksLikedGet());
</script>
<style lang="scss" scoped>
.favorite-tracks-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
