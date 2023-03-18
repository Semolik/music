<template>
    <SetupGenres
        :next-page="!onlyGenres"
        :result-route-name="
            onlyGenres ? 'settings' : routesNames.setupMusicians
        "
    />
</template>
<script setup>
import { routesNames } from "@typed-router";
useHead({ title: "Установка любимых жанров" });
const router = useRouter();

const { onlyGenres } = router.currentRoute.value.query;
definePageMeta({
    layout: "full",
});
</script>
