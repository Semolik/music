<template>
    <div class="musician-tracks-page">
        {{ musician }}
    </div>
</template>
<script setup>
import { Service } from "~/client";
const route = useRoute();
const { id } = route.params;
const musician = await Service.getPublicProfileApiV1MusicianProfileIdInfoGet(
    id
);

useHead({
    title: "Треки исполнителя " + musician.name,
});
definePageMeta({
    getTitle: true,
});
</script>
<style lang="scss" scoped>
.musician-tracks-page {
    color: $primary-text;
}
</style>
