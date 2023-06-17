<template>
    <div class="app-player" v-show="playerStore.current_track_index !== null">
        <AudioPlayer
            ref="player"
            :audio-list="listUrls"
            theme-color="hwb(153 26% 28%)"
            @pause="setPause(true)"
            @play="setPause(false)"
            @ended="handleEnded"
            :show-playback-rate="false"
            :show-play-button="false"
            :show-prev-button="false"
            :show-next-button="false"
            :show-volume-button="false"
            :before-play="handleBeforePlay"
        />
        <div class="player-controls-info" v-if="currentTrack">
            <div class="controls">
                <div
                    class="app-player-button prev"
                    :class="{ disabled: isFirstTrack }"
                >
                    <Icon :name="IconsNames.prevIcon" />
                </div>
                <div
                    class="app-player-button play"
                    @click="playerStore.toggleCurrentTrack"
                >
                    <Icon
                        :name="
                            paused ? IconsNames.playIcon : IconsNames.pauseIcon
                        "
                    />
                </div>
                <div
                    @click="playerStore.nextTrack"
                    class="app-player-button next"
                    :class="{ disabled: isLastTrack }"
                >
                    <Icon :name="IconsNames.nextIcon" />
                </div>
            </div>
            <div class="info">
                <div class="image" @click="playerStore.toggleCurrentTrack">
                    <img :src="currentTrack.picture" />
                    <TrackCardPlayingAnimation :paused="paused" />
                </div>
                <div class="track-info">
                    <div class="track-nanme">
                        {{ currentTrack.name }}
                    </div>
                    <nuxt-link
                        class="musician-name"
                        :to="{
                            name: 'musician-id',
                            params: { id: currentTrack.musician.id },
                        }"
                    >
                        {{ currentTrack.musician.name }}
                    </nuxt-link>
                </div>
            </div>
            <div class="player-end controls">
                <div
                    class="app-player-button"
                    :class="['like', { active: currentTrack.liked }]"
                    @click="playerStore.toggleLike"
                >
                    <Icon :name="IconsNames.likeIcon" />
                </div>
                <div class="app-player-button" @click="menuOpened = true">
                    <Icon :name="IconsNames.dotsIcon" />
                </div>
                <ModalDialog :active="menuOpened" @close="menuOpened = false">
                    <template #content>
                        <div class="menu-modal-items">
                            <TrackCardMenuContent
                                :track="currentTrack"
                                @update:track="playerStore.updateTrack($event)"
                                :addToPlaylistModalOpened="
                                    addToPlaylistModalOpened
                                "
                                @update:addToPlaylistModalOpened="
                                    addToPlaylistModalOpened = $event
                                "
                                v-model:menuOpened="menuOpened"
                                v-model:clipModalOpeneded="clipModalOpeneded"
                                modal-mode
                            />
                        </div>
                    </template>
                </ModalDialog>
            </div>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
import AudioPlayer from "@liripeng/vue-audio-player";
import { usePlayerStore } from "@/stores/player";
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";
import { Service } from "~/client";
const playerStore = usePlayerStore();
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const { listUrls, player, paused, isFirstTrack, currentTrack, isLastTrack } =
    storeToRefs(playerStore);
const setting_pause = ref(false);
const setPause = (value) => {
    setting_pause.value = true;
    paused.value = value;
    setting_pause.value = false;
};
const handleBeforePlay = async (next) => {
    if (logined.value) {
        try {
            await Service.startListeningTrackApiV1TracksTrackIdListeningPost(
                currentTrack.value.id
            );
        } catch (e) {
            console.error(HandleOpenApiError(e).message);
        }
    }
    next();
};
const handleEnded = async () => {
    if (logined.value) {
        try {
            await Service.setListenedTrackApiV1TracksTrackIdListeningPut(
                currentTrack.value.id
            );
        } catch (e) {
            console.error(HandleOpenApiError(e).message);
        }
    }
    playerStore.nextTrack();
};
const addToPlaylistModalOpened = ref(false);
const clipModalOpeneded = ref(false);
watch(paused, (newVal) => {
    if (!setting_pause.value) {
        if (newVal) {
            player.value.pause();
        } else {
            player.value.play();
        }
    }
});
const menuOpened = ref(false);
</script>
<style lang="scss">
.menu-modal-items {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.app-player {
    background-color: $tertiary-bg;
    position: absolute;
    user-select: none;
    left: 0;
    bottom: 0;
    margin: 10px;
    right: 0;
    z-index: 1000;
    border-radius: 15px;
    @include xxl(true) {
        margin: 0;
        border-radius: 0;
    }
    @include lg(true) {
        bottom: 70px;
    }

    .audio-player {
        padding-inline: 20px;
        .audio__progress-wrap {
            margin-top: 20px;
        }
        .audio__notice,
        .audio__btn-wrap,
        .audio__play-loading {
            display: none;
        }
    }
    .player-controls-info {
        padding: 10px;
        display: flex;
        gap: 10px;
        .player-end {
            margin-left: auto;
        }
        .controls {
            display: flex;
            gap: 10px;
            .app-player-button {
                width: 60px;
                height: 60px;
                @include flex-center;
                color: $primary-text;
                border-radius: 10px;
                background-color: $quinary-bg;
                cursor: pointer;

                @include lg(true) {
                    &.next,
                    &.play,
                    &.prev {
                        display: none;
                    }
                }
                &.like.active {
                    color: $accent-red;
                }
                &.disabled {
                    background-color: $quaternary-bg;
                    color: $tertiary-text;
                    cursor: auto;
                    &:hover {
                        background-color: $quaternary-bg;
                    }
                }
                &:hover {
                    background-color: $senary-bg;
                }
                svg {
                    width: 25px;
                    height: 25px;
                }
            }
        }
        .info {
            display: flex;
            gap: 10px;
            color: $primary-text;

            .image {
                width: 60px;
                height: 60px;
                border-radius: 10px;
                overflow: hidden;
                position: relative;
                img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
                .loading-container {
                    @include lg {
                        display: none;
                    }
                }
            }

            .track-info {
                display: flex;
                justify-content: center;
                flex-direction: column;
                overflow: hidden;
                text-overflow: ellipsis;
                .musician-name {
                    color: $secondary-text;
                    &:hover {
                        color: $accent;
                    }
                }
            }
        }
    }
}
</style>
