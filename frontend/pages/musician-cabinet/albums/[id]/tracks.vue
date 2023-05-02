<template>
    <SettingsPage :title="title" max-width="100%" padding="0px">
        <TracksContainer>
            <AlbumUploadTrack
                :track="track"
                v-for="(track, index) in tracks"
                @position-up="positionUp(index)"
                @position-down="positionDown(index)"
                :key="index"
            />
        </TracksContainer>
    </SettingsPage>
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;
const album = ref(await Service.getAlbumByIdApiV1AlbumsAlbumIdGet(id));
const title = computed(
    () => "Редактирование треков альбома " + album.value.name
);
const tracks = ref(album.value.tracks);
const positionUp = (index) => {
    if (index === 0) return;
    const track = tracks.value[index];
    tracks.value.splice(index, 1);
    tracks.value.splice(index - 1, 0, track);
};
const positionDown = (index) => {
    if (index === tracks.value.length - 1) return;
    const track = tracks.value[index];
    tracks.value.splice(index, 1);
    tracks.value.splice(index + 1, 0, track);
};
</script>
