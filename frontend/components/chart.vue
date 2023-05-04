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
            />
        </TracksContainer>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
const viewport = useViewport();
const end = new Date();
const start = new Date(end.getFullYear(), end.getMonth() - 1, end.getDate());
const tracks = ref(
    await Service.getPopularTracksPeriodApiV1TracksPopularPeriodGet(
        start.toISOString(),
        end.toISOString(),
        9,
        1
    )
);
</script>
