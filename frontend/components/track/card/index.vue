<template>
    <card-min
        :picture="track.picture"
        :icon="IconsNames.trackIcon"
        v-bind="$attrs"
        :class="['track-card', { min: min }]"
        @picture-click="handleCardClick"
        @click.self="handleCardClick"
    >
        <template #card-picture v-if="nowPlaying && !createTrackMode">
            <TrackCardPlayingAnimation :paused="paused" />
        </template>
        <template #content>
            <div :class="['info-container', { min: min }]">
                <div class="info" @click="handleCardClick">
                    <span class="track-name">{{ track.name }}</span>
                    <span class="secondary-text musican-name">
                        {{ musicanName }}
                    </span>
                </div>
                <nuxt-link
                    class="info-item album-name"
                    v-if="!min && albumName"
                    :to="albumLink"
                >
                    {{ albumName }}
                </nuxt-link>
                <nuxt-link
                    class="info-item musican-name"
                    v-if="!min && musicanName"
                    :to="musicianLink"
                >
                    {{ musicanName }}
                </nuxt-link>
                <div class="track-dots-button-container">
                    <span class="duration">{{ duration }}</span>
                    <div class="button" @click="toggleLikeTrack" v-if="!min">
                        <Icon
                            :name="IconsNames.likeIcon"
                            :color="track.liked ? 'var(--accent-error)' : null"
                        />
                    </div>
                    <template v-if="createTrackMode">
                        <div class="button" @click="emit('edit')">
                            <Icon :name="IconsNames.pencilIcon" />
                        </div>
                        <div class="button" @click="emit('delete')">
                            <Icon :name="IconsNames.deleteIcon" />
                        </div>
                    </template>
                    <div
                        :class="[
                            'track-dots-button',
                            'button',
                            { active: menuOpened },
                            { 'hide-dots-menu': hideDotsMenu },
                        ]"
                        ref="dotsButton"
                        @click.self="menuOpened = !menuOpened"
                        v-if="!(hideDotsMenu || createTrackMode)"
                    >
                        <Icon :name="IconsNames.dotsIcon" />

                        <div class="menu" v-if="menuOpened">
                            <TrackCardMenuContent
                                :track="track"
                                :addToPlaylistModalOpened="
                                    addToPlaylistModalOpened
                                "
                                :menu-buttons="menuButtons"
                                :musican-info="musicanInfo"
                                @update:addToPlaylistModalOpened="
                                    addToPlaylistModalOpened = $event
                                "
                                v-model:clipModalOpeneded="clipModalOpeneded"
                                v-model:menuOpened="menuOpened"
                                v-model:shareModalOpened="shareModalOpened"
                                @playlist-remove-track="
                                    emit('playlist-remove-track', $event)
                                "
                                @update:track="emit('update:track', $event)"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </card-min>
</template>
<script setup>
import moment from "moment";
import { IconsNames } from "@/configs/icons";
import { usePlayerStore } from "~/stores/player";
import { onClickOutside } from "@vueuse/core";
import { Service } from "@/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { useEventBus } from "@vueuse/core";

const playerStore = usePlayerStore();
const { paused } = storeToRefs(playerStore);
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const emit = defineEmits([
    "update:track",
    "playlist-remove-track",
    "delete",
    "edit",
]);

const {
    track,
    albumInfo,
    min,
    musicanInfo,
    playlistId,
    menuButtons,
    createTrackMode,
    hideDotsMenu,
    onCardClick,
} = defineProps({
    track: {
        type: Object,
        required: true,
    },
    albumInfo: {
        type: Object,
        default: null,
    },
    musicanInfo: {
        type: Object,
        default: null,
    },
    min: {
        type: Boolean,
        default: false,
    },
    playlistId: {
        type: String,
        default: null,
    },
    menuButtons: {
        type: Array,
        default: [],
    },
    createTrackMode: {
        type: Boolean,
        default: false,
    },
    hideDotsMenu: {
        type: Boolean,
        default: false,
    },
    onCardClick: {
        type: Function,
        default: null,
    },
});
const albumLink = computed(() => useAlbumLink(albumInfo, track));
const nowPlaying = computed(() => playerStore.currentTrack?.id === track?.id);
const clipModalOpeneded = ref(false);
const albumName = computed(() => albumInfo?.name || track?.album?.name || null);
const musicianLink = computed(() => useMusicianLink(musicanInfo, track));

const musicanName = computed(
    () =>
        musicanInfo?.name ||
        track?.musician?.name ||
        track?.album?.musician?.name ||
        null
);
const goToLoginBus = useEventBus("go-to-login");
const toggleLikeTrack = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    const liked = await Service.likeTrackApiV1TracksTrackIdLikePut(track.id);
    emit("update:track", { ...track, liked });
};

const addToPlaylistModalOpened = ref(false);
const menuOpened = ref(false);
const shareModalOpened = ref(false);
const dotsButton = ref(null);
const handleCardClick = (event) => {
    if (event.target === dotsButton.value) return;

    if (onCardClick) {
        onCardClick();
        return;
    }
};
onMounted(() => {
    onClickOutside(dotsButton, (event) => {
        if (clipModalOpeneded.value) return;
        if (addToPlaylistModalOpened.value) return;
        if (shareModalOpened.value) return;
        menuOpened.value = false;
    });
});

watch(menuOpened, (value) => {
    if (value) {
        addToPlaylistModalOpened.value = false;
    }
});
const duration = computed(() =>
    moment
        .utc(moment.duration(track.duration, "seconds").asMilliseconds())
        .format("mm:ss")
);
</script>
<style lang="scss" scoped>
.track-card {
    gap: 20px;
    grid-template-columns: min-content 1fr;
    @include lg(true) {
        gap: 10px;
    }
    user-select: none;
    &.min {
        gap: 10px;
        .info-container {
            grid-template-columns: 1fr min-content;
            .info .musican-name {
                display: block;
            }
        }
    }
    .info-container {
        @include flex-center;
        display: grid;
        grid-template-columns: 1fr repeat(3, min-content);
        gap: 20px;
        @include md(true) {
            grid-template-columns: 1fr min-content;
        }

        .info {
            display: flex;
            flex-direction: column;
            margin-right: auto;
            width: 100%;
            overflow: hidden;
            .track-name {
                color: $primary-text;
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }
        }
        .info-item {
            color: $secondary-text;
            @include md(true) {
                display: none;
            }

            @include lg {
                &:hover {
                    color: $primary-text;
                }
            }
            &.track-name,
            &.album-name,
            &.musican-name {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }
        }
    }

    .track-dots-button-container {
        @include flex-center;
        color: $secondary-text;
        gap: 8px;
        &.hide-dots-menu {
            padding-right: 20px;
        }
        .button {
            @include flex-center;
            cursor: pointer;
            border-radius: 50%;
            user-select: none;
            border-radius: 50%;
            @include flex-center;
            position: relative;
            height: min-content;
            padding: 8px;

            svg {
                width: 20px;
                height: 20px;
            }
            &.active {
                background-color: $secondary-bg;
            }
            @include lg {
                &:hover {
                    background-color: $quaternary-bg;
                }
            }

            &::after {
                content: "";
                position: absolute;
                inset: 0;
                border-radius: 50%;
            }
        }

        .track-dots-button {
            svg {
                width: 20px;
                height: 20px;
            }

            .menu {
                position: absolute;
                top: 100%;
                right: 0;
                background-color: $secondary-bg;
                border-radius: 10px;
                padding: 5px;
                display: flex;
                flex-direction: column;
                gap: 5px;
                z-index: 1;
            }
        }
    }
}
</style>
