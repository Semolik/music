<template>
    <div class="albums-page-container">
        <CardsContainer>
            <AlbumCard v-for="album in albums" :album="album" />
        </CardsContainer>
    </div>
</template>
<script setup>
import { Service } from "@/client";

const albums = ref(await Service.getLikedAlbumsApiV1AlbumsLikedGet());
</script>
<style lang="scss" scoped>
.albums-page-container {
    color: $primary-text;
}
</style>
