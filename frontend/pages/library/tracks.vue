<template>
    <ClientOnly>
        <div class="favorite-tracks-container" v-auto-animate>
            <TrackCard
                v-for="(track, index) in tracks"
                :key="track.id"
                v-model:track="tracks[index]"
            />
        </div>
    </ClientOnly>
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
