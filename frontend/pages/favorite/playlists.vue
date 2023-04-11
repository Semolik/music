<template>
    <div class="playlists-contaner">
        <PlaylistCard
            v-for="playlist in playlists"
            :playlist="playlist"
            :key="playlist.id"
            is-link
        />
    </div>
</template>
<script setup>
import { usePlaylistsStore } from "@/stores/playlists";
import { storeToRefs } from "pinia";
const playlistsStore = usePlaylistsStore();
const { playlists } = storeToRefs(playlistsStore);
</script>
<style lang="scss" scoped>
.playlists-contaner {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
    @include lg(true) {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
}
</style>
