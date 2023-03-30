<template>
    <SetupCard
        :picture="genre.picture"
        :name="genre.name"
        @picture-click="likeGenre"
        :liked="genre.liked"
        :icon="IconsNames.guitarIcon"
        overlay-on-like
    />
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { Service } from "@/client";
const emit = defineEmits(["liked", "update:genre"]);
const { genre } = defineProps({
    genre: {
        type: Object,
        required: true,
    },
});

const likeGenre = async () => {
    const liked = await Service.likeGenreApiV1GenresGenreIdLikePut(genre.id);
    emit("liked", liked);
    emit("update:genre", { ...genre, liked });
};
</script>
