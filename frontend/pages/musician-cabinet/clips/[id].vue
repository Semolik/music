<template>
    <ClipPage :id="id" />
</template>
<script setup>
const route = useRoute();
const { id } = route.params;
</script>
