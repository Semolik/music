<template>
    <SetupGenres :next-page="nextPage" />
</template>
<script setup>
import { routesNames } from "@typed-router";
const { nextPage } = defineProps({
    nextPage: {
        type: String,
        default: routesNames.setupMusicians,
    },
});
definePageMeta({
    layout: "full",
});
</script>
