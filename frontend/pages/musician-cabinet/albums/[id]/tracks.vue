<template>
    <SettingsPage :title="title" max-width="100%" padding="0px">
        <TracksContainer>
            <div class="buttons">
                <AppButton active @click="addTrack"> Добавить трек </AppButton>
                <AppButton
                    @[publishButtonActive&&`click`]="
                        publishAlbumModalOpened = true
                    "
                    :active="publishButtonActive"
                >
                    Опубликовать альбом
                </AppButton>
                <ModalDialog
                    :active="publishAlbumModalOpened"
                    @close="publishAlbumModalOpened = false"
                    head-text="Публикация альбома"
                    :buttons="[
                        {
                            text: 'Опубликовать',
                            active: true,
                            onClick: publishAlbum,
                        },
                        {
                            text: 'Отмена',
                            onClick: () => (publishAlbumModalOpened = false),
                        },
                    ]"
                >
                    <template #content>
                        Вы уверены, что хотите опубликовать альбом? <br />После
                        публикации в альбом нельзя будет добавить или удалить из
                        него треки.
                    </template>
                </ModalDialog>
            </div>
            <AlbumUploadTrack
                :track="track"
                :musician-info="musicianProfile"
                v-for="(track, index) in tracks"
                @position-up="positionUp(index)"
                @position-down="positionDown(index)"
                :key="index"
                :album-id="album.id"
                @update="tracks[index] = $event"
                @delete="tracks.splice(index, 1)"
            />
        </TracksContainer>
    </SettingsPage>
</template>
<script setup>
import { Service } from "@/client";
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "@typed-router";
const authStore = useAuthStore();
const { musicianProfile } = storeToRefs(authStore);
const route = useRoute();
const { id } = route.params;
const album = ref(await Service.getAlbumByIdApiV1AlbumsAlbumIdGet(id));
const title = computed(
    () => "Редактирование треков альбома " + album.value.name
);
const tracks = ref(album.value.tracks);
const publishAlbumModalOpened = ref(false);
const router = useRouter();
const publishAlbum = async () => {
    await Service.closeAlbumUploadingApiV1AlbumsAlbumIdCloseUploadingPut(id);
    publishAlbumModalOpened.value = false;
    router.push({
        name: routesNames.musicianCabinet.cabinetAlbumsId,
        params: { id },
    });
};
const publishButtonActive = computed(() => {
    return !!tracks.value.length;
});
const addTrack = () => {
    tracks.value.push({
        name: "",
        duration: 0,
        file: null,
        feat: "",
        new: true,
        picture: null,
        musician: musicianProfile.value,
    });
};
</script>
<style scoped lang="scss">
.buttons {
    display: flex;
    gap: 10px;
    @include lg(true) {
        flex-direction: column;
    }
}
</style>
