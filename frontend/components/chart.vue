<template>
    <Selection
        title="Чарт"
        leftText="Cмотреть все"
        :leftTextLinkName="routesNames.popularTracks"
    >
        <div class="tracks-container">
            <TrackCard
                v-for="track in tracks"
                :key="track.id"
                :track="track"
                class="track-card"
            />
        </div>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
const tracksRaw = await Service.getPopularTracksMonthApiV1TracksPopularMonthGet(
    9,
    1
);
const splice = ref(false);
const viewport = useViewport();
watch(
    viewport.breakpoint,
    () => {
        if (viewport.isLessThan("lg")) {
            splice.value = true;
        } else {
            splice.value = false;
        }
    },
    { immediate: true }
);
const tracks = computed(() => {
    if (splice.value) {
        return tracksRaw.slice(0, 4);
    } else {
        return tracksRaw;
    }
});
</script>
<style lang="scss" scoped>
.tracks-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 10px;
    .track-card {
        flex-grow: 1;
    }
}
</style>
