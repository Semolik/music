<template>
    <TracksContainer animate>
        <TrackCard
            v-for="(history_item, index) in history_tracks"
            :key="history_item.id"
            v-model:track="history_item.track"
            :menu-buttons="[
                {
                    icon: IconsNames.deleteIcon,
                    text: 'Удалить из истории',
                    onClick: () => deleteTrackFromHistory(history_item.id),
                },
            ]"
        />
        <NotFound v-if="!history_tracks.length" />
        <AppButton @click="getNextPage" active v-if="showNextButton">
            Показать ещё
        </AppButton>
    </TracksContainer>
</template>

<script setup>
import { IconsNames } from "~/configs/icons";
import { Service } from "~/client";
import NotFound from "~/components/not-found.vue";
const { HISTORY_ALL_TRACKS_LIMIT } = useRuntimeConfig().public;
useHead({
    title: "История",
});
const history_tracks = ref([]);
const showNextButton = ref(false);
const page = ref(0);
const getNextPage = async () => {
    page.value++;
    const new_history_tracks =
        await Service.getHistoryTracksApiV1HistoryTracksGet(page.value);

    history_tracks.value = history_tracks.value.concat(new_history_tracks);
    showNextButton.value =
        new_history_tracks.length == HISTORY_ALL_TRACKS_LIMIT;
};
getNextPage();
const deleteTrackFromHistory = async (history_item_id) => {
    await Service.deleteTrackFromHistoryApiV1HistoryTracksHistoryItemIdDelete(
        history_item_id
    );
    history_tracks.value = history_tracks.value.filter(
        (history_track) => history_track.id != history_item_id
    );
};
</script>
<style lang="scss" scoped>
.tracks {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
}
</style>
