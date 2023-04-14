<template>
    <div class="album-page-container">
        {{ album }}
    </div>
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;
const album = await Service.getAlbumByIdApiV1AlbumsAlbumIdGet(id);
</script>
<style lang="scss" scoped>
.album-page-container {
    color: $primary-text;
}
</style>
