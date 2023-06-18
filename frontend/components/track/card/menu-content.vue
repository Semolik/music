<template>
    <div
        v-for="item in menuButtons"
        :class="['menu-item', { 'modal-mode': modalMode }]"
    >
        <Icon :name="item.icon" />
        <span @click="item.onClick">
            {{ item.text }}
        </span>
    </div>
    <div
        :class="['menu-item', { 'modal-mode': modalMode }]"
        v-if="playlistId && logined"
    >
        <Icon :name="IconsNames.deleteIcon" />
        <span @click="removeTrackFromPlaylist"> Удалить из плейлиста </span>
    </div>
    <div
        :class="['menu-item like', { 'modal-mode': modalMode }]"
        @click="toggleLikeTrack"
    >
        <Icon
            :name="track.liked ? IconsNames.dislikeIcon : IconsNames.likeIcon"
        />
        <span>
            {{ track.liked ? "Удалить из избранного" : "Добавить в избранное" }}
        </span>
    </div>
    <div
        v-if="!playlistId && logined"
        :class="['menu-item', { 'modal-mode': modalMode }]"
        @click="openAddToPlaylistModal"
    >
        <Icon :name="IconsNames.plusIcon" />
        <span> Добавить в плейлист </span>
    </div>
    <nuxt-link
        :to="albumLink"
        :class="['menu-item', { 'modal-mode': modalMode }]"
        @click="menuOpened = false"
    >
        <Icon :name="IconsNames.albumIcon" />
        <span>Перейти к альбому</span>
    </nuxt-link>

    <nuxt-link
        :to="musicianLink"
        :class="['menu-item', { 'modal-mode': modalMode }]"
        @click="menuOpenedLocal = false"
    >
        <Icon :name="IconsNames.userIcon" />
        <span>Перейти к исполнителю</span>
    </nuxt-link>
    <template v-if="track.clip">
        <div
            :class="['menu-item', { 'modal-mode': modalMode }]"
            @click="clipModalOpenededLocal = true"
        >
            <Icon :name="IconsNames.clipIcon" />
            <span>Клип</span>
        </div>
        <ClipModal
            :modalOpened="clipModalOpeneded"
            @update:modalOpened="clipModalOpenededLocal = $event"
            :clip="track.clip"
            @update:clip="
                emit('update:track', {
                    ...track,
                    clip: $event,
                })
            "
        />
    </template>
    <div
        :class="['menu-item', { 'modal-mode': modalMode }]"
        @click="
            () => {
                emit('update:shareModalOpened', true);
            }
        "
    >
        <Icon :name="IconsNames.shareIcon" />
        <span>Поделиться</span>
    </div>
    <ModalDialog
        :active="addToPlaylistModalOpened"
        :head-text="createMode ? 'Создание плейлиста' : 'Добавление в плейлист'"
        @close="closeAddToPlaylistModal"
        key="playlist-modal"
        close-on-esckey
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
                <PlaylistCreateModalContent
                    v-if="createMode"
                    @creared="closeAddToPlaylistModal"
                />
                <template v-else>
                    <div class="playlists">
                        <PlaylistCard
                            v-for="playlist in playlistsStore.playlists"
                            :key="playlist.id"
                            :playlist="playlist"
                            min
                            hide-end-icon
                            class="playlist-card"
                            @card-click="addTrackToPlaylist(playlist.id)"
                        >
                            <template #card-end>
                                <div class="add-remove-button-container">
                                    <div
                                        :class="[
                                            'add-remove-button',
                                            { remove: false },
                                        ]"
                                    >
                                        <Icon :name="IconsNames.plusIcon" />
                                    </div>
                                </div>
                            </template>
                        </PlaylistCard>
                    </div>
                </template>
            </div>
        </template>
    </ModalDialog>
    <ShareTrackModal
        :active="shareModalOpened"
        @update:active="emit('update:shareModalOpened', $event)"
        :track="track"
    />
</template>
<script setup>
import { usePlaylistsStore } from "@/stores/playlists";
import { useEventBus } from "@vueuse/core";
import { IconsNames } from "@/configs/icons";
import { Service } from "@/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const { $toast } = useNuxtApp();

const playlistsStore = usePlaylistsStore();
const {
    track,
    playlistId,
    menuButtons,
    createTrackMode,
    addToPlaylistModalOpened,
    menuOpened,
    musicanInfo,
    albumInfo,
    clipModalOpeneded,
    modalMode,
    shareModalOpened,
} = defineProps({
    track: {
        type: Object,
        required: true,
    },
    musicanInfo: {
        type: Object,
        required: false,
    },
    playlistId: {
        type: String,
        default: null,
    },
    menuButtons: {
        type: Array,
        default: [],
    },
    addToPlaylistModalOpened: {
        type: Boolean,
        default: false,
    },
    createTrackMode: {
        type: Boolean,
        default: false,
    },
    menuOpened: {
        type: Boolean,
        default: false,
    },
    albumInfo: {
        type: Object,
        required: false,
    },
    clipModalOpeneded: {
        type: Boolean,
        default: false,
    },
    modalMode: {
        type: Boolean,
        default: false,
    },
    shareModalOpened: {
        type: Boolean,
        default: false,
    },
});
const musicianLink = computed(() => useMusicianLink(musicanInfo, track));
const albumLink = computed(() => useAlbumLink(albumInfo, track));

const goToLoginBus = useEventBus("go-to-login");
const toggleLikeTrack = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    const liked = await Service.likeTrackApiV1TracksTrackIdLikePut(track.id);
    emit("update:track", { ...track, liked });
};
const clipModalOpenededLocal = computed({
    get: () => clipModalOpeneded,
    set: (value) => {
        console.log(value);
        emit("update:clipModalOpeneded", value);
    },
});
const emit = defineEmits([
    "update:addToPlaylistModalOpened",
    "update:menuOpened",
    "update:track",
    "playlist-remove-track",
    "update:clipModalOpeneded",
    "update:shareModalOpened",
]);

const route = useRoute();
watch(route, () => {
    addToPlaylistModalOpenedLocal.value = false;
    menuOpenedLocal.value = false;
});
const addToPlaylistModalOpenedLocal = computed({
    get: () => addToPlaylistModalOpened,
    set: (value) => {
        emit("update:addToPlaylistModalOpened", value);
    },
});
const menuOpenedLocal = computed({
    get: () => menuOpened,
    set: (value) => {
        emit("update:menuOpened", value);
    },
});
const createMode = ref(false);
const removeTrackFromPlaylist = async () => {
    try {
        menuOpenedLocal.value = false;
        await playlistsStore.removeTrackFromPlaylist({
            playlistId,
            trackId: track.id,
        });
        emit("playlist-remove-track", track.id);
    } catch (e) {
        $toast.error("Не удалось удалить трек из плейлиста");
    }
};

const openAddToPlaylistModal = () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    addToPlaylistModalOpenedLocal.value = true;
};

const closeAddToPlaylistModal = () => {
    menuOpenedLocal.value = false;
    addToPlaylistModalOpenedLocal.value = false;
};
watch(addToPlaylistModalOpenedLocal, (value) => {
    createMode.value = false;
    if (value) {
        menuOpenedLocal.value = false;
    }
});

const addTrackToPlaylist = async (playlistId) => {
    try {
        await playlistsStore.addTrackToPlaylist({
            playlistId,
            trackId: track.id,
        });
    } catch (e) {
        $toast.error(HandleOpenApiError(e).message);
    }

    addToPlaylistModalOpenedLocal.value = false;
};
</script>
<style lang="scss" scoped>
.menu-item {
    display: grid;
    grid-template-columns: 20px 1fr;
    gap: 5px;
    color: $secondary-text;
    white-space: nowrap;
    cursor: pointer;
    border-radius: 5px;
    padding: 5px 10px;
    @include lg {
        &:hover {
            background-color: $quaternary-bg;

            &.modal-mode {
                background-color: $quinary-bg;
            }
        }
    }
    svg {
        width: 20px;
        height: 20px;
        margin: auto;
    }
    &.like {
        min-width: 230px;
    }
    &.modal-mode {
        padding: 10px 20px;
        background-color: $quaternary-bg;
        flex-grow: 1;
        text-align: center;
    }
}
.playlist-modal-content {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .playlists {
        display: flex;
        flex-direction: column;
        gap: 10px;
        min-height: 300px;
        overflow: hidden;

        .playlist-card {
            @include lg {
                &:hover {
                    .add-remove-button-container {
                        .add-remove-button {
                            &.remove {
                                background-color: $accent-red;
                                svg {
                                    color: $primary-bg;
                                }
                            }
                            background-color: $accent;
                            svg {
                                color: $primary-bg;
                            }
                        }
                    }
                }
            }
            .add-remove-button-container {
                @include flex-center;

                .add-remove-button {
                    @include flex-center;
                    border-radius: 50%;
                    padding: 10px;
                    background-color: $quinary-bg;
                    aspect-ratio: 1/1;
                    svg {
                        color: $secondary-text;
                        width: 20px;
                        height: 20px;
                    }
                }
            }
        }
    }
}
</style>
