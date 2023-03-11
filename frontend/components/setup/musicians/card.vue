<template>
    <SetupCard
        :picture="musician.picture"
        :name="musician.name"
        @picture-click="likeMusician"
        :liked="liked"
        :icon="IconsNames.userIcon"
        overlay-on-like
    />
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { Service } from "@/client";
const emit = defineEmits(["liked"]);
const { musician } = defineProps({
    musician: {
        type: Object,
        required: true,
    },
});
const liked = ref(musician.liked);
const likeMusician = async () => {
    liked.value = await Service.likeMusicianApiV1MusicianProfileIdLikePut(
        musician.id
    );
    emit("liked", liked.value);
};
</script>
