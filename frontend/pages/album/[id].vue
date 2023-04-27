<template>
    <ContentHead
        :name="album.name"
        :picture="album.picture"
        :icon="IconsNames.albumIcon"
        :info="info"
        type="Альбом"
        :is-owner="isOwner"
        @edit="editAlbum"
        :is-liked="album.liked"
        @like="toggleLikeAlbum"
        hide-delete-button
        :likes-count="album.likes_count"
    >
        <div class="tracks">
            <TrackCard
                v-for="(track, index) in album.tracks"
                :key="track.id"
                v-model:track="album.tracks[index]"
                :album-info="album"
                :musican-info="album.musician"
            />
        </div>
    </ContentHead>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~/configs/icons";
import { useAuthStore } from "~/stores/auth";
import { routesNames } from "@typed-router";
import { storeToRefs } from "pinia";
import { useEventBus } from "@vueuse/core";
const goToLoginBus = useEventBus("go-to-login");
definePageMeta({
    disableDefaultLayoutPadding: true,
});
const route = useRoute();
const { id } = route.params;
const album = ref(await Service.getAlbumByIdApiV1AlbumsAlbumIdGet(id));

const authStore = useAuthStore();
const { logined, musicianProfile } = storeToRefs(authStore);

const isOwner = computed(
    () =>
        musicianProfile.value &&
        musicianProfile.value.id === album.value.musician.id
);
const toggleLikeAlbum = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    const { liked, likes_count } =
        await Service.albumLikeApiV1AlbumsAlbumIdLikePut(id);
    album.value.liked = liked;
    album.value.likes_count = likes_count;
};

const info = computed(() => [
    {
        name: "Исполнитель:",
        value: album.value.musician.name,
        link: {
            name: "musician-id",
            params: { id: album.value.musician.id },
        },
    },
    {
        value: album.value.year,
    },
]);
const router = useRouter();
const editAlbum = () => {
    router.push({
        name: routesNames.musicianCabinet.cabinetAlbumsId,
        params: { id: album.value.id },
    });
};
</script>
<style lang="scss" scoped>
.tracks {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
