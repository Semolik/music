<template>
    <card-min v-bind="props" v-if="min">
        <template #content>
            <span>{{ musician.name }}</span>
        </template>
        <template #card-end>
            <div class="flex justify-center items-center pr-4 secondary-text">
                <Icon name="material-symbols:arrow-forward-ios" />
            </div>
        </template>
    </card-min>
    <div class="musician-card" v-else>
        <card-picture v-bind="props">
            <div class="hover-overlay">
                <div
                    :class="[
                        'favorite',
                        'button',
                        { active: liked },
                        { disabled: !logined },
                    ]"
                    @click="onFavorite"
                >
                    <Icon :name="likeIcon" />
                </div>
                <div class="play button">
                    <Icon :name="playIcon" />
                </div>
                <div class="more button">
                    <Icon :name="dotsIcon" />
                </div>
            </div>
        </card-picture>
        <div class="flex flex-col grow text-center">
            {{ musician.name }}
        </div>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { useEventBus } from "@vueuse/core";
import { IconsNames } from "@/configs/icons";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);

const { likeIcon, playIcon, dotsIcon } = IconsNames;
const goToLoginBus = useEventBus("go-to-login");
const { musician } = defineProps({
    musician: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
});

const liked = ref(musician.liked);

const props = reactive({
    picture: musician.picture,
    icon: IconsNames.musicianIcon,
    borderRadius: "50%",
});
const onFavorite = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    liked.value = await Service.likeMusicianApiV1MusicianProfileIdLikePut(
        musician.id
    );
};
</script>
<style lang="scss" scoped>
.musician-card {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .hover-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
        @include flex-center;
        gap: 5px;
        .button {
            border-radius: 50%;
            @include flex-center;
            height: min-content;
            padding: 5px;
            width: 35px;
            height: 35px;
            transition: background-color 0.2s ease-in-out;
            svg {
                height: 100%;
                width: 100%;
            }
            &.play {
                background-color: $accent;
                width: 50px;
                height: 50px;
                &:hover {
                    background-color: $accent-hover;
                }
                svg {
                    color: black;
                }
            }
            &.favorite {
                &:not(.disabled).active {
                    svg {
                        color: $accent-2;
                    }
                }

                &.disabled {
                    background-color: $secondary-bg;

                    &:hover {
                        background-color: $secondary-bg;
                    }
                }
            }
            background-color: $tertiary-bg;
            cursor: pointer;
            &:hover {
                background-color: $quaternary-bg;
            }
        }
    }
    &:hover .hover-overlay {
        opacity: 1;
    }
}
</style>
