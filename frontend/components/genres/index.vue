<template>
    <Selection
        title="Жанры"
        description="Выберите любимый жанр и начните слушать музыку"
        leftText="Все жанры"
        :leftTextLink="{ name: 'genres' }"
    >
        <GenresList :genres="genres" one-line />
    </Selection>
</template>
<script setup>
import { routesNames } from "@typed-router";
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
