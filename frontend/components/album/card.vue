<template>
    <card
        :text="album.name"
        :picture="album.picture"
        icon="material-symbols:album"
    />
</template>
<script setup>
const { album } = defineProps({
    album: {
        type: Object,
        required: true,
    },
});
</script>
