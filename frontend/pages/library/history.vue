<template>
    <div class="tracks">
        <TrackCard
            v-for="(track, index) in tracks"
            :key="track.id"
            v-model:track="tracks[index]"
        />
        <AppButton @click="getNextPage" active v-if="showNextButton">
            Показать ещё
        </AppButton>
    </div>
</template>

<script setup>
import { Service } from "~/client";
const { HISTORY_ALL_TRACKS_LIMIT } = useRuntimeConfig().public;
useHead({
    title: "История",
});
const tracks = ref([]);
const showNextButton = ref(false);
const page = ref(0);
const getNextPage = async () => {
    page.value++;
    const new_tracks = await Service.getHistoryTracksApiV1HistoryTracksGet(
        page.value
    );
    tracks.value = tracks.value.concat(new_tracks);
    showNextButton.value = new_tracks.length == HISTORY_ALL_TRACKS_LIMIT;
};
getNextPage();
</script>
<style lang="scss" scoped>
.tracks {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
