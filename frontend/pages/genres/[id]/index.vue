<template>
    <ContentHead
        :name="genre.name"
        :picture="genre.picture"
        type="Жанр"
        :is-liked="genre.liked"
        @like="like"
        :hide-play-button="notFound || !genre.popular_tracks.length"
        @play="playGenre"
    >
        <div class="genre-page">
            <Selection
                title="Популярные треки"
                left-text="Все треки"
                :left-text-link="{
                    name: routesNames.genresId.idTracks,
                    params: { id: genre.id },
                }"
                v-if="genre.popular_tracks.length"
            >
                <TracksContainer grid cut>
                    <TrackCard
                        v-for="(track, index) in genre.popular_tracks"
                        :key="track.id"
                        v-model:track="genre.popular_tracks[index]"
                        min
                        :onCardClick="() => playTrack(track)"
                    />
                </TracksContainer>
            </Selection>
            <Selection
                title="Популярные музыканты"
                left-text="Все музыканты"
                :left-text-link="{
                    name: routesNames.genresId.idMusicians,
                    params: { id: genre.id },
                }"
                v-if="genre.popular_musicians.length"
            >
                <CardsContainer>
                    <MusicianCard
                        v-for="(musician, index) in genre.popular_musicians"
                        :key="musician.id"
                        v-model:musician="genre.popular_musicians[index]"
                        is-link
                    />
                </CardsContainer>
            </Selection>
            <Selection
                title="Популярные альбомы"
                left-text="Все альбомы"
                :left-text-link="{
                    name: routesNames.genresId.idAlbums,
                    params: { id: genre.id },
                }"
                v-if="genre.popular_albums.length"
            >
                <CardsContainer>
                    <AlbumCard
                        v-for="(album, index) in genre.popular_albums"
                        :key="album.id"
                        v-model:album="genre.popular_albums[index]"
                    />
                </CardsContainer>
            </Selection>
            <Selection
                title="Новые альбомы"
                left-text="Все альбомы"
                :left-text-link="{
                    name: routesNames.genresId.idNewAlbums,
                    params: { id: genre.id },
                }"
                v-if="genre.new_albums.length"
            >
                <CardsContainer>
                    <AlbumCard
                        v-for="(album, index) in genre.new_albums"
                        :key="album.id"
                        v-model:album="genre.new_albums[index]"
                    />
                </CardsContainer>
            </Selection>
            <NotFound
                v-if="notFound"
                text="Контента с таким жанром не найдено"
            />
        </div>
    </ContentHead>
</template>
<script setup>
import { routesNames } from "@typed-router";
import { Service } from "~~/client";
import { usePlayerStore } from "~/stores/player";
const playerStore = usePlayerStore();
definePageMeta({
    disableDefaultLayoutPadding: true,
});
const route = useRoute();
const { id } = route.params;
const genre = ref(await Service.getGenreApiV1GenresGenreIdGet(id));
const like = async () => {
    genre.value.liked = await Service.likeGenreApiV1GenresGenreIdLikePut(id);
};
const notFound = computed(
    () =>
        !genre.value.new_albums.length &&
        !genre.value.popular_albums.length &&
        !genre.value.popular_musicians.length &&
        !genre.value.popular_tracks.length
);
const playTrack = (track) => {
    playerStore.setTracks(genre.value.popular_tracks, track);
    playerStore.toggleCurrentTrack();
};
const playGenre = () => {
    if (!genre.value.popular_tracks.length) return;
    playTrack(genre.value.popular_tracks[0]);
};
</script>
<style lang="scss" scoped>
.genre-page {
    display: flex;
    flex-direction: column;
    gap: 20px;
    height: 100%;
    padding: 20px;
}
</style>
