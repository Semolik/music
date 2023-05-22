<template>
    <Selection
        title="Чарт"
        leftText="Cмотреть все"
        :leftTextLink="{ name: routesNames.popularTracks.index }"
    >
        <TracksContainer grid cut>
            <TrackCard
                v-for="(track, index) in tracks"
                :track="track"
                @update:track="tracks[index] = $event"
                class="track-card"
                min
                :onCardClick="() => playTrack(track)"
            />
        </TracksContainer>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
import { usePlayerStore } from "~/stores/player";
const playerStore = usePlayerStore();
const end = new Date();
const start = new Date(end.getFullYear(), end.getMonth() - 1, end.getDate());
const tracks = ref(
    await Service.getPopularTracksPeriodApiV1TracksPopularPeriodGet(
        start.toISOString(),
        end.toISOString(),
        8,
        1
    )
);
const playTrack = (track) => {
    playerStore.setTracks(tracks.value, track);
    playerStore.toggleCurrentTrack();
};
</script>
