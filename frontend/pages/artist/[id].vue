<template>
    <div class="artist-page-container">
        {{ artist }}
    </div>
</template>
<script setup>
import { Service } from "@/client";
const route = useRoute();
const { id } = route.params;
const artist = await Service.getPublicProfileInfoApiV1MusicianProfileIdGet(id);
</script>
<style lang="scss" scoped>
.artist-page-container {
    color: $primary-text;
}
</style>
