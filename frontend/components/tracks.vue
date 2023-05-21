<template>
    <ItemsPaginate v-bind="$attrs" is-tracks>
        <template v-slot="{ items }">
            <TrackCard
                v-for="(track, index) in items"
                :key="track.id"
                v-model:track="items[index]"
                :onCardClick="() => playTrack(track, items)"
            />
        </template>
    </ItemsPaginate>
</template>
<script setup>
import { usePlayerStore } from "~/stores/player";
const playerStore = usePlayerStore();
const playTrack = (track, tracks) => {
    playerStore.setTracks(tracks, track);
    playerStore.toggleCurrentTrack();
};
</script>
