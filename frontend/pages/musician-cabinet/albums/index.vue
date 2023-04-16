<template>
    <div class="albums-page-container">
        <AddSearch
            v-model:search="search"
            placeholder="Поиск по вашим альбомам"
            :to="{ name: 'musician-cabinet-albums-add' }"
        />
        <CardsContainer>
            <AlbumCard v-for="album in albums" :key="album.id" :album="album" />
        </CardsContainer>
        <NotFound :text="notFoundAlbumsMessage" v-if="notFoundAlbums" />
    </div>
</template>

<script setup>
import { Service } from "@/client";
const my_albums = await Service.getMyAlbumsApiV1AlbumsMyGet();
const albums = ref(my_albums);
const search = ref("");
const fetching = ref(false);
const notFoundAlbums = computed(() => {
    if (fetching.value) return false;

    return albums.value.length === 0;
});
const notFoundAlbumsMessage = computed(() => {
    if (search.value === "") return "У вас нет альбомов";
    return null;
});
watch(search, async (value) => {
    if (value === "") {
        albums.value = my_albums;
        return;
    }
    albums.value = await Service.searchMyAlbumsApiV1AlbumsMySearchGet(value);
});
</script>
