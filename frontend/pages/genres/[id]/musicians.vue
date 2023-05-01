<template>
    <Musicians
        :on-next-page="loadMore"
        :page_size="POPULAR_MUSICIANS_LIMIT_ALL"
    />
</template>
<script setup>
const route = useRoute();
const { id } = route.params;
import { Service } from "@/client";
const { POPULAR_MUSICIANS_LIMIT_ALL } = useRuntimeConfig().public;
const loadMore = async (page) => {
    return await Service.getPopularMusiciansByGenreIdApiV1GenresGenreIdMusiciansGet(
        id,
        page.value
    );
};
</script>
