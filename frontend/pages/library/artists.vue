<template>
    <Musicians :on-next-page="loadMore" :page-size="FAVORITE_MUSICIANS_LIMIT" />
</template>
<script setup>
import { Service } from "~/client";
const { FAVORITE_MUSICIANS_LIMIT } = useRuntimeConfig().public;

const loadMore = async (page) => {
    return await Service.getLikedMusicianProfilesApiV1MusicianLikedGet(
        page.value
    );
};
</script>
<style lang="scss" scoped>
.favorite-musicians {
    display: flex;
    flex-direction: column;
    height: 100%;
}
</style>
