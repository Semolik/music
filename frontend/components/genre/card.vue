<template>
    <div class="genre-card">
        <card-picture v-bind="propsBind" @click="likeGenre">
            <div :class="['hover-overlay', { force: forceOverlay }]">
                <div :class="['like-button', { active: liked }]">
                    <Icon :name="IconsNames.likeIcon" />
                </div>
            </div>
        </card-picture>
        <div class="genre-name">
            <span>{{ genre.name }}</span>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { Service } from "~~/client";
const emit = defineEmits(["update:genre"]);
const { genre, forceOverlay } = defineProps({
    genre: {
        type: Object,
        required: true,
    },
    forceOverlay: {
        type: Boolean,
        required: false,
        default: false,
    },
});
const liked = ref(genre.liked);
const likeGenre = async () => {
    liked.value = await Service.likeGenreApiV1GenresGenreIdLikePut(genre.id);
};

const propsBind = reactive({
    picture: genre.picture,
    borderRadius: "50%",
    icon: IconsNames.guitarIcon,
});
</script>
<style lang="scss" scoped>
.genre-card {
    display: flex;
    flex-direction: column;
    gap: 15px;
    position: relative;

    .hover-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.5);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;

        &.force,
        &:hover {
            opacity: 1;
        }

        .like-button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: $accent;
            cursor: pointer;
            transition: 0.2s;
            &:hover {
                background-color: $accent-hover;
            }
            &.active {
                background-color: $quaternary-bg;
                svg {
                    color: red;
                }
            }
            svg {
                color: black;
                width: 100%;
                height: 100%;
            }
        }
    }

    .genre-name {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
        span {
            font-weight: 500;
        }
    }
}
</style>
