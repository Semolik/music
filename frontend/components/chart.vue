<template>
    <Selection
        title="Чарт"
        leftText="Cмотреть все"
        :leftTextLinkName="routesNames.popularTracks"
    >
        <div class="tracks-container">
            <TrackCard
                v-for="(track, index) in tracks"
                :key="track.id"
                v-model:track="tracks[index]"
                class="track-card"
            />
        </div>
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
const tracksRaw = ref(
    await Service.getPopularTracksMonthApiV1TracksPopularMonthGet(9, 1)
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
const tracks = computed({
    get() {
        if (splice.value) {
            return tracksRaw.value.slice(0, 4);
        } else {
            return tracksRaw.value;
        }
    },
    set(val) {
        if (splice.value) {
            tracksRaw.value = tracksRaw.value.map((track, index) => {
                if (index < 4) {
                    return val[index];
                } else {
                    return track;
                }
            });
        } else {
            tracksRaw.value = val;
        }
    },
});
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
