<template>
    <SetupGenres :next-page="nextPage" :result-route-name="resultRouteName" />
</template>
<script setup>
import { routesNames } from "@typed-router";
const { nextPage, resultRouteName } = defineProps({
    nextPage: {
        type: Boolean,
        default: true,
    },
    resultRouteName: {
        type: String,
        default: routesNames.setupMusicians,
    },
});
definePageMeta({
    layout: "full",
});
</script>
