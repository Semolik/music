<template>
    <div class="popular-tracks-page">
        <div class="tracks">
            <TrackCard
                v-for="(track, index) in tracks"
                :key="track.id"
                :track="track"
                @update:track="tracks[index] = $event"
                is-link
            />
        </div>
        <AppButton v-if="showMoreButton" @click="getTracks">
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~/client";
const { period } = defineProps({
    period: {
        type: String,
        required: true,
    },
});
const { POPULAR_TRACKS_LIMIT } = useRuntimeConfig().public;
const page = ref(0);
const tracks = ref([]);
const showMoreButton = ref(false);
const period_start = computed(() => {
    var period_end = new Date();
    switch (period) {
        case "month":
            return new Date(
                period_end.getFullYear(),
                period_end.getMonth() - 1,
                period_end.getDate()
            );
        case "week":
            return new Date(
                period_end.getFullYear(),
                period_end.getMonth(),
                period_end.getDate() - 7
            );
    }
});
const period_end = computed(() => new Date());
const getTracks = async () => {
    page.value++;
    var new_tracks;
    if (period === "all") {
        new_tracks = await Service.getPopularTracksApiV1TracksPopularGet(
            page.value,
            POPULAR_TRACKS_LIMIT
        );
    } else {
        new_tracks =
            await Service.getPopularTracksPeriodApiV1TracksPopularPeriodGet(
                period_start.value.toISOString(),
                period_end.value.toISOString(),
                POPULAR_TRACKS_LIMIT,
                page.value
            );
    }
    tracks.value = tracks.value.concat(new_tracks);
    showMoreButton.value = new_tracks.length === POPULAR_TRACKS_LIMIT;
};
await getTracks();
</script>
<style lang="scss" scoped>
.popular-tracks-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .tracks {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
