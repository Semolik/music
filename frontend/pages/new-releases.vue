<template>
    <Albums :on-next-page="loadMore" :page-size="LAST_ALBUMS_LIMIT" />
</template>
<script setup>
import { Service } from "~/client";
import { useHeaderStore } from "~/stores/header";
const headerStore = useHeaderStore();
definePageMeta({
    title: "Новые релизы",
});
headerStore.setTitle("Новые релизы");

const { LAST_ALBUMS_LIMIT } = useRuntimeConfig().public;
const loadMore = async (page) => {
    return await Service.getLastAlbumsApiV1AlbumsLastGet(
        page.value,
        LAST_ALBUMS_LIMIT
    );
};
loadMore();
</script>
