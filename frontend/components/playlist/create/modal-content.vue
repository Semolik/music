<template>
    <div class="create-playlist">
        <AppInput
            placeholder="Название плейлиста"
            v-model="newPlaylistName"
            class="playlist-name"
            :max-length="MAX_PLAYLIST_NAME_LENGTH"
            show-word-limit
            autofocus
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
            border-radius="5px"
        >
            Создать
        </AppButton>
    </div>
</template>
<script setup>
const { MAX_PLAYLIST_NAME_LENGTH } = useRuntimeConfig().public;
import { Service } from "~~/client";
const { track_id } = defineProps({
    track_id: {
        type: String,
        required: false,
    },
});
const newPlaylistName = ref("");
const newPlaylistPublic = ref(false);
const newPlaylistButtonActive = computed(() => {
    return newPlaylistName.value.length > 0;
});
const emit = defineEmits(["creared"]);
const createPlaylist = async () => {
    if (!newPlaylistButtonActive.value) return;
    const playlist = await Service.createPlaylistApiV1PlaylistsPost({
        tracks_ids: track_id ? [track_id] : [],
        name: newPlaylistName.value,
        description: null,
        private: !newPlaylistPublic.value,
    });
    emit("creared", playlist);
};
</script>
<style scoped lang="scss">
.create-playlist {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .playlist-name {
        --app-input-border-radius: 5px;
    }
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
</style>
