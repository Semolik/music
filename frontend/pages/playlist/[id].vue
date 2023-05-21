<template>
    <ContentHead
        :name="playlist.name"
        :picture="playlist.picture"
        :icon="IconsNames.playlistIcon"
        :info="info"
        type="Плейлист"
        :is-owner="isOwner"
        @edit="openEditModal"
        @delete="openDeleteModal"
        :is-liked="playlist.liked"
        @like="toggleLikePlaylist"
        :hide-play-button="!playButtonActive"
        @play="playPlaylist"
    >
        <div
            :class="['description', { splitter: !playlist.picture }]"
            v-if="playlist.description"
        >
            {{ playlist.description }}
        </div>
        <div class="playlist-tracks">
            <TrackCard
                v-for="(track, index) in playlist.tracks"
                :key="track.id"
                v-model:track="playlist.tracks[index]"
                :playlist-id="playlist.id"
                @playlist-remove-track="playlist.tracks.splice(index, 1)"
                :onCardClick="() => playTrack(track)"
            />
            <NotFound v-if="!playlist.tracks.length" text="Плейлист пуст" />
        </div>
    </ContentHead>
    <ModalDialog
        :active="editModalOpened"
        @close="editModalOpened = false"
        head-text="Редактирование плейлиста"
        :buttons="[
            {
                text: 'Отмена',
                onClick: () => (editModalOpened = false),
            },
            {
                text: 'Сохранить',
                active: saveButtonIsActive,
                onClick: updatePlaylist,
            },
        ]"
    >
        <template #content>
            <AppInput
                v-model="newPlaylistName"
                label="Название плейлиста"
                :error="newPlaylistNameError"
                :max-length="MAX_PLAYLIST_NAME_LENGTH"
                show-word-limit
            />
            <AppInput
                v-model="newPlaylistDescription"
                label="Описание плейлиста"
                :max-length="MAX_PLAYLIST_DESCRIPTION_LENGTH"
                show-word-limit
                type="textarea"
                rows="8"
                resize="none"
            />
            <div class="private-switch">
                <AppSwitch
                    v-model="newPlaylistPrivate"
                    active-text="Публичный"
                    inactive-text="Приватный"
                />
            </div>
        </template>
    </ModalDialog>
    <ModalDialog
        :active="deleteModalOpened"
        @close="deleteModalOpened = false"
        head-text="Удаление плейлиста"
        :buttons="[
            {
                text: 'Отмена',
                onClick: () => (deleteModalOpened = false),
            },
            {
                text: 'Удалить',
                active: true,
                onClick: deletePlaylist,
            },
        ]"
    >
        <template #content>
            <div class="delete-modal-text">
                Вы действительно хотите удалить плейлист {{ playlist.name }}?
            </div>
        </template>
    </ModalDialog>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~/configs/icons";
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "@typed-router";
import { useEventBus } from "@vueuse/core";
import { usePlayerStore } from "~/stores/player";
const route = useRoute();
const playerStore = usePlayerStore();

const goToLoginBus = useEventBus("go-to-login");
const { MAX_PLAYLIST_NAME_LENGTH, MAX_PLAYLIST_DESCRIPTION_LENGTH } =
    useRuntimeConfig().public;
definePageMeta({
    disableDefaultLayoutPadding: true,
});
const router = useRouter();
const { id } = route.params;
const playlist = ref(
    await Service.getPlaylistInfoApiV1PlaylistsPlaylistIdGet(id)
);
useHead({
    title: "Плейлист " + playlist.value.name,
});
const playTrack = async (track) => {
    playerStore.setTracks(playlist.value.tracks, track);
    playerStore.toggleCurrentTrack();
};
const playButtonActive = computed(() => playlist.value.tracks.length > 0);
const playPlaylist = async () => {
    if (!playButtonActive.value) {
        return;
    }

    playTrack(playlist.value.tracks[0]);
};
const authStore = useAuthStore();
const { userData, logined } = storeToRefs(authStore);
const isOwner = computed(
    () => logined.value && userData.value.id === playlist.value.user.id
);
const editModalOpened = ref(false);
const deleteModalOpened = ref(false);
const openEditModal = () => {
    deleteModalOpened.value = false;
    editModalOpened.value = true;
};
const toggleLikePlaylist = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    playlist.value.liked =
        await Service.likePlaylistApiV1PlaylistsPlaylistIdLikePut(id);
};
const openDeleteModal = () => {
    editModalOpened.value = false;
    deleteModalOpened.value = true;
};
const newPlaylistName = ref(playlist.value.name);
const newPlaylistDescription = ref(playlist.value.description || "");
const newPlaylistNameError = computed(() => newPlaylistName.value.length === 0);
const newPlaylistPrivate = ref(playlist.value.private);

watch(editModalOpened, (value) => {
    if (!value) {
        newPlaylistName.value = playlist.value.name;
        newPlaylistDescription.value = playlist.value.description || "";
        newPlaylistPrivate.value = playlist.value.private;
    }
});
const playlistDescriptionChanged = computed(() => {
    if (
        newPlaylistDescription.value === "" &&
        playlist.value.description === null
    ) {
        return false;
    }
    return newPlaylistDescription.value !== playlist.value.description;
});
const saveButtonIsActive = computed(
    () =>
        !newPlaylistNameError.value &&
        (newPlaylistName.value !== playlist.value.name ||
            playlistDescriptionChanged.value ||
            newPlaylistPrivate.value !== playlist.value.private)
);
const updatePlaylist = async () => {
    if (!saveButtonIsActive.value) {
        return;
    }
    const data = {
        name: newPlaylistName.value,
        description: newPlaylistDescription.value,
        private: newPlaylistPrivate.value,
    };
    playlist.value = await Service.updatePlaylistApiV1PlaylistsPlaylistIdPut(
        id,
        data
    );
    editModalOpened.value = false;
};
const deletePlaylist = async () => {
    await Service.deletePlaylistApiV1PlaylistsPlaylistIdDelete(id);
    router.push({ name: routesNames.library.playlists });
};
const tracks_word = usePluralize(playlist.value.tracks_count, [
    "трек",
    "трека",
    "треков",
]);
const userName = computed(() => useFullName(playlist.value.user));
const info = computed(() => [
    {
        name: "Автор:",
        value: userName.value,
        link: {
            name: "user-id",
            params: { id: playlist.value.user.id },
        },
    },
    {
        name: null,
        value: `${playlist.value.tracks_count} ${tracks_word}`,
    },
]);
</script>
<style lang="scss" scoped>
.private-switch {
    @include flex-center;
}
.playlist-tracks {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    padding: 10px;
}
.description {
    padding: 10px;
    background-color: $tertiary-bg;

    &.splitter {
        border-top: 1px solid $quinary-bg;
    }
}
</style>
