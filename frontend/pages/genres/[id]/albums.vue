<template>
    <Albums :on-next-page="loadMore" :limit="POPULAR_ALBUMS_LIMIT_ALL" />
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;

const { POPULAR_ALBUMS_LIMIT_ALL } = useRuntimeConfig().public;
const loadMore = async (page) => {
    return await Service.getPopularAlbumsByGenreIdApiV1GenresGenreIdAlbumsGet(
        id,
        page.value
    );
};
</script>
