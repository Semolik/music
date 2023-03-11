<template>
    <SetupCard
        :picture="genre.picture"
        :name="genre.name"
        @picture-click="likeGenre"
        :liked="liked"
        :icon="IconsNames.guitarIcon"
        overlay-on-like
    />
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { Service } from "@/client";
const emit = defineEmits(["liked"]);
const { genre } = defineProps({
    genre: {
        type: Object,
        required: true,
    },
});
const liked = ref(genre.liked);
const likeGenre = async () => {
    liked.value = await Service.likeGenreApiV1GenresGenreIdLikePut(genre.id);
    emit("liked", liked.value);
};
</script>
