<template>
    <div class="track-page-container">
        <div class="track-info-container">
            <div class="controls">
                <div class="button" @click="shareTrackModalOpened = true">
                    <Icon :name="IconsNames.shareIcon" />
                </div>
                <ShareTrackModal
                    v-model:active="shareTrackModalOpened"
                    :track="track"
                />
                <div class="button play">
                    <Icon :name="IconsNames.playIcon" />
                </div>
                <div
                    :class="['button like', { active: track.liked }]"
                    @click="likeTrack"
                >
                    <Icon :name="IconsNames.likeIcon" />
                </div>
            </div>
            <InfoItems :items="items" />
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~~/configs/icons";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { useEventBus } from "@vueuse/core";
const goToLoginBus = useEventBus("go-to-login");
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const route = useRoute();
const { id } = route.params;
const track = ref(await Service.getTrackApiV1TracksTrackIdGet(id));
const shareTrackModalOpened = ref(false);
const likeTrack = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    track.value.liked = await Service.likeTrackApiV1TracksTrackIdLikePut(
        track.value.id
    );
};
const items = [
    {
        title: "Название",
        value: track.value.name,
    },
    {
        to: { name: "album-id", params: { id: track.value.album.id } },
        title: "Альбом",
        value: track.value.album.name,
    },
    {
        to: {
            name: "musician-id",
            params: { id: track.value.musician.id },
        },
        title: "Исполнитель",
        value: track.value.musician.name,
    },
];
</script>
<style lang="scss" scoped>
.track-page-container {
    @include flex-center;
    height: 100%;
    .track-info-container {
        min-width: 400px;

        padding: 20px;
        border-radius: 30px;
        background-color: $tertiary-bg;
        display: flex;
        flex-direction: column;
        gap: 20px;
        .controls {
            @include flex-center;
            gap: 10px;
            .button {
                @include flex-center;
                border-radius: 50%;
                background-color: $senary-bg;
                cursor: pointer;
                transition: 0.2s;
                width: 50px;
                height: 50px;
                scale: 1;

                &.like.active {
                    color: $accent-error;
                }

                @include lg {
                    &:hover {
                        scale: 1.05;
                    }
                }
                &.play {
                    width: 100px;
                    height: 100px;
                    background-color: $accent;

                    svg {
                        width: 40px;
                        height: 40px;
                    }
                }

                .icon {
                    width: 30px;
                    height: 30px;
                }
            }
        }
    }
}
</style>
