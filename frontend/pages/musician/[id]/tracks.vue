<template>
    <div class="musician-tracks-page">
        <div class="tracks">
            <TrackCard
                v-for="(track, index) in tracks"
                :key="track.id"
                :track="track"
                @update:track="tracks[index] = $event"
            />
        </div>
        <AppButton
            @click="fetchTracks"
            class="show-more-button"
            active
            v-if="showMoreButton"
        >
            Показать еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~/client";
const { MUSICIAN_ALL_TRACKS_LIMIT } = useRuntimeConfig().public;
const route = useRoute();
const { id } = route.params;
const musician = await Service.getPublicProfileApiV1MusicianProfileIdInfoGet(
    id
);
const tracks = ref([]);
const page = ref(0);
const showMoreButton = ref(false);
const fetchTracks = async () => {
    page.value += 1;
    const new_tracks =
        await Service.getMusicianPopularTracksApiV1MusicianProfileIdPopularGet(
            id,
            page.value
        );
    tracks.value = [...tracks.value, ...new_tracks];
    showMoreButton.value = new_tracks.length === MUSICIAN_ALL_TRACKS_LIMIT;
};
fetchTracks();
useHead({
    title: "Треки исполнителя " + musician.name,
});
definePageMeta({
    getTitle: true,
});
</script>
<style lang="scss" scoped>
.musician-tracks-page {
    color: $primary-text;
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
