<template></template>
<script setup>
import { Service } from "~~/client";
const route = useRoute();
const { id } = route.params;
const genre = await Service.getGenreApiV1GenresGenreIdGet(id);
</script>
