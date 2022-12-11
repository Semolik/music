<template>
    <div class="liked-tracks-container">
        <Track v-for="track in tracks" :key="track.id" :trackData="track" />
    </div>
</template>
<script setup>
import { HTTP } from "/src/http-common.vue";
import { ref } from "vue";
import Track from "/src/components/Track.vue";
var tracks = ref([]);
const getLikedTracks = async (page) => {
    const { data } = await HTTP.get("/tracks/liked", {
        params: {
            page: page,
        },
    });
    tracks.value = [...tracks.value, ...data];
};
getLikedTracks(1);
</script>
<style lang="scss">
.liked-tracks-container {
}
</style>
