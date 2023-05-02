<template>
    <SettingsPage :title="title" max-width="100%" padding="0px"> </SettingsPage>
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;
const album = ref(await Service.getAlbumByIdApiV1AlbumsAlbumIdGet(id));
const title = computed(
    () => "Редактирование треков альбома " + album.value.name
);
</script>
