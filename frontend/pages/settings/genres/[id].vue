<template>
    <GenresPage :id="id" />
</template>
<script setup>
definePageMeta({
    middleware: ["admin"],
});
const router = useRouter();
const { id } = router.currentRoute.value.params;
</script>
