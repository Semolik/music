<template>
    <Selection
        title="Чарт"
        leftText="Cмотреть все"
        :leftTextLinkName="routesNames.popularTracks"
    >
        <div class="tracks-container">
            <TrackCard
                v-for="(track, index) in showedTracks"
                :track="track"
                @update:track="tracksRaw[index] = $event"
                class="track-card"
                min
            />
        </div>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
const viewport = useViewport();

const tracksRaw = ref(
    await Service.getPopularTracksMonthApiV1TracksPopularMonthGet(9, 1)
);

const showedTracks = ref([]);
watch(
    viewport.breakpoint,
    () => {
        if (viewport.isLessThan("lg")) {
            showedTracks.value = tracksRaw.value.slice(0, 4);
        } else {
            showedTracks.value = tracksRaw.value;
        }
    },
    { immediate: true }
);
</script>
<style lang="scss" scoped>
.tracks-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    grid-template-rows: min-content;
    @include lg(true) {
        grid-template-columns: 1fr;
    }
    gap: 10px;
    .track-card {
        flex-grow: 1;
    }
}
</style>
