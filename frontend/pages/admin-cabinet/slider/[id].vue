<template>
    <SliderPage :id="id" />
</template>
<script setup>
const route = useRoute();
const id = route.params.id;
</script>
