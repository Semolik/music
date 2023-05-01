<template>
    <div :class="['genres-container', { 'one-line': oneLine }, { cut: cut }]">
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
    oneLine: {
        type: Boolean,
        required: false,
        default: false,
    },
    cut: {
        type: Boolean,
        required: false,
        default: false,
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
    &.one-line {
        grid-auto-rows: 0px;
        grid-template-rows: 1fr;
        overflow-y: hidden;
    }

    &.cut {
        @include xl(true) {
            .genre-card:nth-child(n + 5) {
                display: none;
            }
        }
    }
}
</style>
