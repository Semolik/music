<template>
    <div class="genre-page-container">
        {{ genre }}
    </div>
</template>
<script setup>
import { Service } from "~~/client";
const route = useRoute();
const { id } = route.params;
const genre = await Service.getGenreApiV1GenresGenreIdGet(id);
</script>
<style lang="scss" scoped>
.genre-page-container {
    color: $primary-text;
}
</style>
