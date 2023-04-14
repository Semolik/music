<template>
    <card-min
        :picture="track.picture"
        :icon="IconsNames.trackIcon"
        v-bind="$attrs"
        :class="['track-card', { min: min }]"
    >
        <template #content>
            <div :class="['info-container', { min: min }]">
                <div class="info">
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
                    <span>{{ duration }}</span>
                    <div class="button" @click="toggleLikeTrack" v-if="!min">
                        <Icon
                            :name="IconsNames.likeIcon"
                            :color="track.liked ? 'var(--accent-error)' : null"
                        />
                    </div>
                    <div
                        :class="[
                            'track-dots-button',
                            'button',
                            { active: menuOpened },
                        ]"
                        ref="card"
                        @click.self="menuOpened = !menuOpened"
                    >
                        <Icon :name="IconsNames.dotsIcon" />
                        <div class="menu" v-if="menuOpened">
                            <div
                                class="menu-item like"
                                @click="toggleLikeTrack"
                            >
                                <Icon
                                    :name="
                                        track.liked
                                            ? IconsNames.dislikeIcon
                                            : IconsNames.likeIcon
                                    "
                                    :color="
                                        track.liked
                                            ? 'var(--accent-error)'
                                            : null
                                    "
                                />
                                <span>
                                    {{
                                        track.liked
                                            ? "Удалить из избранного"
                                            : "Добавить в избранное"
                                    }}
                                </span>
                            </div>
                            <nuxt-link
                                :to="albumLink"
                                class="menu-item"
                                @click="menuOpened = false"
                            >
                                <Icon :name="IconsNames.albumIcon" />
                                <span>Перейти к альбому</span>
                            </nuxt-link>
                            <nuxt-link
                                :to="musicianLink"
                                class="menu-item"
                                @click="menuOpened = false"
                            >
                                <Icon :name="IconsNames.userIcon" />
                                <span>Перейти к исполнителю</span>
                            </nuxt-link>
                            <div
                                class="menu-item"
                                @click="openAddToPlaylistModal"
                            >
                                <Icon :name="IconsNames.plusIcon" />
                                <span> Добавить в плейлист </span>
                            </div>
                            <div
                                class="menu-item"
                                @click="
                                    () => {
                                        menuOpened = false;
                                        shareModalOpened = true;
                                    }
                                "
                            >
                                <Icon :name="IconsNames.shareIcon" />
                                <span>Поделиться</span>
                            </div>
                        </div>
                        <ShareTrackModal
                            :active="shareModalOpened"
                            @update:active="shareModalOpened = $event"
                            :track="track"
                        />
                    </div>
                </div>
            </div>
        </template>
        <template #card-end> </template>
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
</template>
<script setup>
import moment from "moment";
import { IconsNames } from "@/configs/icons";
import { usePlaylistsStore } from "@/stores/playlists";
import { onClickOutside } from "@vueuse/core";
import { Service } from "@/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { useEventBus } from "@vueuse/core";
import { useToast } from "vue-toastification";
const playlistsStore = usePlaylistsStore();
const toast = useToast();
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);

const { track, albumInfo, min, musicanInfo } = defineProps({
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
});
const albumLink = computed(() => {
    var album_id = track?.album?.id || albumInfo?.id;
    if (!album_id) return null;
    return {
        name: "album-id",
        params: { id: album_id },
    };
});
const albumName = computed(() => albumInfo?.name || track?.album?.name || null);
const musicianLink = computed(() => {
    var musician_id =
        track?.musician?.id ||
        musicanInfo?.id ||
        track?.album?.musician?.id ||
        null;
    if (!musician_id) return null;
    return {
        name: "artist-id",
        params: { id: musician_id },
    };
});
const emit = defineEmits(["update:track"]);
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
const shareModalOpened = ref(false);
const addToPlaylistModalOpened = ref(false);
const card = ref(null);
const menuOpened = ref(false);
const createMode = ref(false);
const newPlaylistName = ref("");
const newPlaylistPublic = ref(false);
const newPlaylistButtonActive = computed(() => {
    return newPlaylistName.value.length > 0;
});
watch(menuOpened, (value) => {
    if (value) {
        addToPlaylistModalOpened.value = false;
    }
});
const openAddToPlaylistModal = () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    addToPlaylistModalOpened.value = true;
};
watch(addToPlaylistModalOpened, (value) => {
    createMode.value = false;
    newPlaylistName.value = "";
    newPlaylistPublic.value = false;
    if (value) {
        menuOpened.value = false;
    }
});

const addTrackToPlaylist = async (playlistId) => {
    try {
        await playlistsStore.addTrackToPlaylist({
            playlistId,
            trackId: track.id,
        });
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }

    addToPlaylistModalOpened.value = false;
};
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
.track-card {
    gap: 20px;
    grid-template-columns: min-content 1fr;
    @include lg(true) {
        gap: 10px;
    }
    &.min {
        gap: 10px;
        .info-container .info .musican-name {
            display: block;
        }
    }
    .info-container {
        @include flex-center;
        gap: 30px;

        .info {
            display: flex;
            flex-direction: column;
            margin-right: auto;
            .track-name {
                color: $primary-text;
            }
            .musican-name {
                @include lg {
                    display: none;
                }
            }
        }
        .info-item {
            color: $secondary-text;
            @include md(true) {
                &.album-name,
                &.musican-name {
                    display: none;
                }
            }

            @include lg {
                &:hover {
                    color: $primary-text;
                }
            }
        }
    }

    .track-dots-button-container {
        @include flex-center;
        color: $secondary-text;
        gap: 8px;

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
                }
            }
        }
    }
}
</style>
