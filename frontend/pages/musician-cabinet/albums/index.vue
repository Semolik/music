<template>
    <div class="albums-page-container">
        <AddSearch
            v-model:search="search"
            placeholder="Поиск по вашим альбомам"
            :to="{ name: 'musician-cabinet-albums-add' }"
        />
        <CardsContainer>
            <AlbumCard
                v-for="album in albums"
                :key="album.id"
                :album="album"
                disable-link
                @click="goToAlbum(album)"
            />
        </CardsContainer>
        <NotFound :text="notFoundAlbumsMessage" v-if="notFoundAlbums" />
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { routesNames } from "@typed-router";
const my_albums = await Service.getMyAlbumsApiV1AlbumsMyGet();
const albums = ref(my_albums);
const search = ref("");
const fetching = ref(false);
const notFoundAlbums = computed(() => {
    if (fetching.value) return false;
    return albums.value.length === 0;
});
const goToAlbum = (album) => {
    router.push({
        name: routesNames.musicianCabinet.cabinetAlbumsId,
        params: { id: album.id },
    });
};
const router = useRouter();
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
<style lang="scss" scoped>
.albums-page-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
}
</style>
