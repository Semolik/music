<template>
    <card-min
        ref="card"
        :picture="track.picture"
        :icon="IconsNames.trackIcon"
        v-bind="$attrs"
    >
        <template #content>
            <span>{{ track.name }}</span>
            <span class="secondary-text">{{ track.album.musician.name }}</span>
        </template>
        <template #card-end>
            <div class="track-dots-button-container">
                <span>{{ duration }}</span>
                <div
                    :class="['track-dots-button', { active: menuOpened }]"
                    @click.self="menuOpened = !menuOpened"
                >
                    <Icon :name="dotsIcon" />
                    <div class="menu" v-if="menuOpened">
                        <div
                            class="menu-item"
                            @click="addToPlaylistModalOpened = true"
                        >
                            <Icon :name="IconsNames.plusIcon" />
                            <span> Добавить в плейлист </span>
                        </div>
                        <div class="menu-item" @click="toggleLikeTrack">
                            <Icon
                                :name="
                                    track.liked
                                        ? IconsNames.dislikeIcon
                                        : IconsNames.likeIcon
                                "
                                :color="
                                    track.liked ? 'var(--accent-error)' : null
                                "
                            />
                            <span>
                                {{
                                    track.liked
                                        ? "Убрать из избранного"
                                        : "Добавить в избранное"
                                }}
                            </span>
                        </div>

                        <div class="menu-item">
                            <Icon :name="IconsNames.shareIcon" />
                            <span> Поделиться </span>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </card-min>
    <ModalDialog
        :active="addToPlaylistModalOpened"
        :head-text="createMode ? 'Создание плейлиста' : 'Добавление в плейлист'"
        @close="
            () => {
                menuOpened = false;
                addToPlaylistModalOpened = false;
            }
        "
    >
        <template #content>
            <div class="playlist-modal-content">
                <AppButton
                    active
                    :no-accent="createMode"
                    @click="createMode = !createMode"
                >
                    <span>
                        {{ createMode ? "Назад" : "Создать новый плейлист" }}
                    </span>
                </AppButton>
                <div class="create-playlist" v-if="createMode">
                    <AppInput
                        placeholder="Название плейлиста"
                        v-model="newPlaylistName"
                    />
                    <div class="playlist-type">
                        <span class="playlist-type-text"> Тип плейлиста </span>
                        <AppSwitch
                            active-text="Публичный"
                            inactive-text="Приватный"
                            v-model="newPlaylistPublic"
                        />
                    </div>

                    <AppButton
                        :active="newPlaylistButtonActive"
                        @click="createPlaylist"
                    >
                        Создать
                    </AppButton>
                </div>
                <template v-else>
                    <div class="playlists">
                        <PlaylistCard
                            v-for="playlist in playlistsStore.playlists"
                            :key="playlist.id"
                            :playlist="playlist"
                            min
                        />
                    </div>
                </template>
            </div>
        </template>
    </ModalDialog>
</template>
<script setup>
import moment from "moment";

import { IconsNames } from "@/configs/icons";
import { usePlaylistsStore } from "@/stores/playlists";
import { onClickOutside } from "@vueuse/core";
import { Service } from "@/client";
const { track } = defineProps({
    track: {
        type: Object,
        required: true,
    },
});
const emit = defineEmits(["update:track"]);
const playlistsStore = usePlaylistsStore();
const toggleLikeTrack = async () => {
    const liked = await Service.likeTrackApiV1TracksTrackIdLikePut(track.id);
    emit("update:track", { ...track, liked });
};
const addToPlaylistModalOpened = ref(false);
const card = ref(null);
const menuOpened = ref(false);
const createMode = ref(false);
const newPlaylistName = ref("");
const newPlaylistPublic = ref(false);
const newPlaylistButtonActive = computed(() => {
    return newPlaylistName.value.length > 0;
});
watch(addToPlaylistModalOpened, (value) => {
    createMode.value = false;
    newPlaylistName.value = "";
    newPlaylistPublic.value = false;
    if (value) {
        menuOpened.value = false;
    }
});
const createPlaylist = async () => {
    await playlistsStore.createPlaylist({
        name: newPlaylistName.value,
        is_public: newPlaylistPublic.value,
        trackIds: [track.id],
    });
    addToPlaylistModalOpened.value = false;
};
onMounted(() => {
    onClickOutside(card, () => {
        menuOpened.value = false;
    });
});
const { dotsIcon } = IconsNames;

const duration = computed(() =>
    moment
        .utc(moment.duration(track.duration, "seconds").asMilliseconds())
        .format("mm:ss")
);
</script>
<style lang="scss" scoped>
.playlist-modal-content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .playlists {
        display: flex;
        flex-direction: column;
        gap: 10px;
        min-height: 300px;
    }
    .create-playlist {
        display: flex;
        flex-direction: column;
        gap: 10px;
        .playlist-type {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: auto;
            .playlist-type-text {
                font-size: 14px;
                color: $secondary-text;
            }
        }
    }
}
.track-dots-button-container {
    @include flex-center;
    color: $secondary-text;
    gap: 8px;
    padding-right: 0.5rem;
    .track-dots-button {
        user-select: none;
        border-radius: 50%;
        @include flex-center;
        position: relative;
        height: min-content;
        padding: 8px;
        &.active {
            background-color: $secondary-bg;
        }
        &:hover {
            background-color: $quaternary-bg;
        }
        &::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 50%;
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
            .menu-item {
                display: grid;
                grid-template-columns: 20px 1fr;
                gap: 5px;
                color: $secondary-text;
                white-space: nowrap;
                cursor: pointer;
                border-radius: 5px;
                padding: 5px 10px;
                &:hover {
                    background-color: $quaternary-bg;
                }
                svg {
                    width: 20px;
                    height: 20px;
                    margin: auto;
                }
            }
        }
    }
}
</style>
