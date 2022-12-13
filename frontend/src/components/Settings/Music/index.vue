<template>
    <div class="liked-tracks-container">
        <Track v-for="track in tracks" :key="track.id" :trackData="track" />
        <div class="empty-tracks" v-if="tracksIsEmpty">
            Список избранных треков пуст
        </div>
    </div>
</template>
<script setup>
import { HTTP } from "/src/http-common.vue";
import { ref } from "vue";
import Track from "/src/components/Track.vue";
import { computed } from "vue";
var tracks = ref([]);
const getLikedTracks = async (page) => {
    const { data } = await HTTP.get("/tracks/liked", {
        params: {
            page: page,
        },
    });
    tracks.value = [...tracks.value, ...data];
};
const tracksIsEmpty = computed(() => tracks.value.length === 0);
getLikedTracks(1);
</script>
<style lang="scss">
@use "@/assets/styles/helpers";
.liked-tracks-container {
    display: flex;
    height: 100%;
    flex-direction: column;
}
.empty-tracks {
    @include helpers.flex-center;
    border: 2px dashed var(--color-text);
    height: 100%;
    border-radius: 10px;
}
</style>
