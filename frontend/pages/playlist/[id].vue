<template>
    <div class="playlist-page-container">
        {{ playlist }}
        <div class="playlist-tracks">
            <TrackCard
                v-for="(track, index) in playlist.tracks"
                :key="track.id"
                v-model:track="playlist.tracks[index]"
                album-info
            />
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;
const playlist = ref(
    await Service.getPlaylistInfoApiV1PlaylistsPlaylistIdGet(id)
);
</script>
<style lang="scss" scoped>
.playlist-page-container {
    color: $primary-text;
    .playlist-tracks {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
