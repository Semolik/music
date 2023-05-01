<template>
    <TracksContainer>
        <TrackCard
            v-for="(track, index) in tracks"
            :key="track.id"
            v-model:track="tracks[index]"
        />
        <NotFound v-if="!tracks.length && !fetching" />
        <AppButton v-if="loadMoreButton">Загрузить еще</AppButton>
    </TracksContainer>
</template>
<script setup>
const { onNextPage, page_size } = defineProps({
    onNextPage: {
        type: Function,
        required: true,
    },
    page_size: {
        type: Number,
        required: true,
    },
});
const tracks = ref([]);
const page = ref(0);
const loadMoreButton = ref(false);
const fetching = ref(false);
const loadMore = async () => {
    fetching.value = true;
    page.value++;
    const new_tracks = await onNextPage(page.value);
    tracks.value = tracks.value.concat(new_tracks);
    loadMoreButton.value = new_tracks.length == page_size;
    fetching.value = false;
};
loadMore();
</script>
