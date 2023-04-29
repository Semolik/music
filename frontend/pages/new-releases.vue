<template>
    <div class="new-releases-page">
        <CardsContainer>
            <AlbumCard
                v-for="album in albums"
                :key="album.id"
                :album="album"
                is-link
            />
        </CardsContainer>
        <AppButton
            v-if="loadMoreButton"
            class="load-more-button"
            @click="loadMore"
        >
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~/client";
definePageMeta({
    title: "Новые релизы",
});
const albums = ref([]);
const loadMoreButton = ref(false);
const page = ref(0);
const { LAST_ALBUMS_LIMIT } = useRuntimeConfig().public;
const loadMore = async () => {
    page.value++;
    const new_albums = await Service.getLastAlbumsApiV1AlbumsLastGet(
        page.value,
        LAST_ALBUMS_LIMIT
    );
    loadMoreButton.value = new_albums.length === LAST_ALBUMS_LIMIT;
    albums.value = albums.value.concat(new_albums);
};
loadMore();
</script>
