<template>
    <div class="genres-container">
        <GenresCard
            v-for="genre in genres"
            :key="genre.id"
            :genre="genre"
            class="genre-card"
            min
        />
    </div>
</template>
<script setup>
defineProps({
    genres: {
        type: Array,
        required: true,
    },
});
</script>
<style scoped lang="scss">
.genres-container {
    display: grid;
    --size: 200px;
    @include sm(true) {
        --size: 160px;
    }
    grid-template-columns: repeat(auto-fill, minmax(var(--size), 1fr));
    gap: 10px;
}
</style>
