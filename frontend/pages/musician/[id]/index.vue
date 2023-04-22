<template>
    <ContentHead
        :name="musician.name"
        :picture="musician.picture"
        :icon="IconsNames.userIcon"
        type="Музыкант"
        :is-owner="isOwner"
        @edit="goToEditPage"
        :is-liked="musician.liked"
        @like="toggleLikeMusician"
        is-musician
        hide-delete-button
        :likes-count="musician.likes_count"
        play-button-text="Перемешать"
    >
        <div class="musician-page-content">
            <selection
                title="Популярные треки"
                leftTextLinkName="musician-id-tracks"
                left-text="Все треки"
                :left-text-link-params="{ id: musician.id }"
                v-if="musician.popular.tracks.length"
            >
                <div class="popular-tracks">
                    <TrackCard
                        v-for="track in musician.popular.tracks"
                        :track="track"
                        @update:track="musician.tracks[index] = $event"
                    />
                </div>
            </selection>
            <selection
                title="Популярные альбомы"
                leftTextLinkName="musician-id-albums"
                left-text="Все альбомы"
                :left-text-link-params="{ id: musician.id }"
                v-if="musician.popular.albums.length"
            >
                <CardsContainer>
                    <AlbumCard
                        v-for="album in musician.popular.albums"
                        :album="album"
                        @update:album="musician.albums[index] = $event"
                        :musician-info="musician"
                    />
                </CardsContainer>
            </selection>
            <selection
                title="Клипы"
                leftTextLinkName="musician-id-clips"
                left-text="Все клипы"
                :left-text-link-params="{ id: musician.id }"
                v-if="musician.popular.clips.length"
            >
                {{ musician.popular.clips }}
            </selection>
        </div>
    </ContentHead>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
import { Service } from "@/client";
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "@typed-router";
import { useEventBus } from "@vueuse/core";

const goToLoginBus = useEventBus("go-to-login");
const route = useRoute();
const { id } = route.params;
const musician = ref(
    await Service.getPublicProfileInfoApiV1MusicianProfileIdGet(id)
);
definePageMeta({
    disableDefaultLayoutPadding: true,
});
useHead({
    title: musician.value.name,
});
const authStore = useAuthStore();
const { musicianProfile, logined } = storeToRefs(authStore);
const isOwner = computed(
    () => logined.value && musicianProfile.value.id === musician.value.id
);
const router = useRouter();
const goToEditPage = () => {
    router.push({
        name: routesNames.musicianCabinet.cabinetProfile,
    });
};
const toggleLikeMusician = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    const { liked, likes_count } =
        await Service.likeMusicianApiV1MusicianProfileIdLikePut(id);

    musician.value.liked = liked;
    musician.value.likes_count = likes_count;
};
</script>
<style lang="scss" scoped>
.musician-page-content {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    .popular-tracks {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
