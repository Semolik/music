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
        @play="playMusician"
    >
        <div class="musician-page-content">
            <selection
                title="Популярные треки"
                left-text="Все треки"
                :left-text-link="{
                    name: routesNames.musicianId.idTracks,
                    params: { id: musician.id },
                }"
                v-if="musician.popular.tracks.length"
            >
                <TracksContainer grid :animate="false">
                    <TrackCard
                        v-for="(track, index) in musician.popular.tracks"
                        :track="track"
                        @update:track="musician.popular.tracks[index] = $event"
                        min
                        :musican-info="musician"
                        :onCardClick="() => playTrack(track)"
                    />
                </TracksContainer>
            </selection>
            <selection
                title="Популярные альбомы"
                left-text="Все альбомы"
                :left-text-link="{
                    name: routesNames.musicianId.idAlbums,
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
                    name: routesNames.musicianId.idClips,
                    params: { id: musician.id },
                }"
                v-if="musician.popular.clips.length"
            >
                <SliderSwiper class="slider" :loop="false" :autoplay="false">
                    <SwiperSlide
                        v-for="(clip, index) in musician.popular.clips"
                        :key="clip.id"
                        class="slide"
                    >
                        <ClipCard
                            v-model:clip="musician.popular.clips[index]"
                            :musician-info="musician"
                        />
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
import { usePlayerStore } from "~/stores/player";
const playerStore = usePlayerStore();
const goToLoginBus = useEventBus("go-to-login");
const route = useRoute();
const { id } = route.params;
const musician = ref(
    await Service.getPublicProfileInfoApiV1MusicianProfileIdGet(id)
);
const tracksWithMusician = computed(() =>
    musician.value.popular.tracks.map((track) => ({
        ...track,
        musician: musician.value,
    }))
);
const playTrack = (track) => {
    playerStore.setTracks(tracksWithMusician.value, track);
    playerStore.toggleCurrentTrack();
};
const playMusician = () => {
    if (!tracksWithMusician.value.length) return;
    playTrack(tracksWithMusician.value[0]);
};
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
}
.slider {
    width: 100%;
    .slide {
        max-width: 300px;
    }
}
</style>
