<template>
    <Clips :on-next-page="loadMore" :page_size="CLIP_PAGE_COUNT" />
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;
const { CLIP_PAGE_COUNT } = useRuntimeConfig().public;
const loadMore = async (page) => {
    return await Service.getMusicianClipsApiV1MusicianProfileIdClipsGet(
        id,
        page.value
    );
};
</script>
