<template>
    <div class="favorite-tracks-container">
        <TrackCard v-for="track in tracks" :key="track.id" :track="track" />
    </div>
</template>
<script setup>
import { Service } from "@/client";
const tracks = await Service.getLikedTracksApiV1TracksLikedGet();
</script>
