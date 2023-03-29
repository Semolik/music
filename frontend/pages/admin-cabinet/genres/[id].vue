<template>
    <GenresCreatePage :id="id" />
</template>
<script setup>
definePageMeta({
    middleware: ["admin"],
});
const route = useRoute();
const { id } = route.params;
</script>
