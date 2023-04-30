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
                left-text="Все треки"
                :left-text-link="{
                    name: routesNames.musicianIdTracks,
                    params: { id: musician.id },
                }"
                v-if="musician.popular.tracks.length"
            >
                <div class="popular-tracks">
                    <TrackCard
                        v-for="(track, index) in musician.popular.tracks"
                        :track="track"
                        @update:track="musician.popular.tracks[index] = $event"
                        min
                        :musican-info="musician"
                        class="track-card"
                    />
                </div>
            </selection>
            <selection
                title="Популярные альбомы"
                left-text="Все альбомы"
                :left-text-link="{
                    name: routesNames.musicianIdAlbums,
                    params: { id: musician.id },
                }"
                v-if="musician.popular.albums.length"
            >
                <CardsContainer one-line>
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
                left-text="Все клипы"
                :left-text-link="{
                    name: routesNames.musicianIdClips,
                    params: { id: musician.id },
                }"
                v-if="musician.popular.clips.length"
            >
                <SliderSwiper class="slider" :loop="false" :autoplay="false">
                    <SwiperSlide
                        v-for="clip in musician.popular.clips"
                        :key="clip.id"
                        class="slide"
                    >
                        <ClipCard :clip="clip" :musician-info="musician" />
                    </SwiperSlide>
                </SliderSwiper>
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
    () =>
        musicianProfile.value && musicianProfile.value.id === musician.value.id
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

    @include lg(true) {
        padding: 10px;
        padding-top: 20px;
    }
    .popular-tracks {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        grid-template-rows: min-content;
        height: min-content;
        @include lg(true) {
            grid-template-columns: 1fr;
        }
        gap: 10px;
        .track-card {
            flex-grow: 1;
        }
    }
}
.slider {
    width: 100%;
    .slide {
        max-width: 300px;
    }
}
</style>