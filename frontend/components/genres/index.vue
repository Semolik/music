<template>
    <Selection
        title="Жанры"
        description="Выберите любимый жанр и начните слушать музыку"
        leftText="Все жанры"
        leftTextLinkName="genres"
    >
        <GenresList :genres="genres" />
    </Selection>
</template>
<script setup>
import { Service } from "~~/client";
const { all } = defineProps({
    all: {
        type: Boolean,
        required: false,
        default: true,
    },
});
const genres = await Service.getGenresApiV1GenresGet();
</script>
<style lang="scss" scoped></style>
