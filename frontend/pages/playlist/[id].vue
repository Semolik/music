<template>
    <div class="playlist-page-container">
        <div class="playlist-info">
            <div
                :class="[
                    'playlist-info-bg',
                    { 'no-picture': !playlist.picture },
                ]"
            >
                <img
                    class="playlist-info-bg"
                    :src="playlist.picture"
                    v-if="playlist.picture"
                />
            </div>
            <div class="playlist-picture">
                <img :src="playlist.picture" v-if="playlist.picture" />
                <div class="icon" v-else>
                    <Icon :name="IconsNames.playlistIcon" />
                </div>
            </div>
            <div class="playlist-info-content">
                <div class="info-line">ПЛЕЙЛИСТ</div>
                <div class="playlist-name">
                    {{ playlist.name }}
                </div>
                <div class="info-line">
                    Составитель:
                    <div class="value">{{ userName }}</div>
                    <div class="dot"></div>
                    <div class="value">
                        {{ playlist.tracks_count }} тре{{ track_word_end }}
                    </div>
                </div>
            </div>
        </div>
        <div class="playlist-tracks">
            <TrackCard
                v-for="(track, index) in playlist.tracks"
                :key="track.id"
                v-model:track="playlist.tracks[index]"
                album-info
                :playlist-id="playlist.id"
                @playlist-remove-track="playlist.tracks.splice(index, 1)"
            />
        </div>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~/configs/icons";
definePageMeta({
    disableDefaultLayoutPadding: true,
});

const route = useRoute();
const { id } = route.params;
const playlist = ref(
    await Service.getPlaylistInfoApiV1PlaylistsPlaylistIdGet(id)
);
const track_word_end = usePluralize(playlist.value.tracks_count, [
    "к",
    "ка",
    "ков",
]);
const userName = computed(() => useFullName(playlist.value.user));
</script>
<style lang="scss" scoped>
.playlist-page-container {
    display: flex;
    flex-direction: column;
    color: $primary-text;
    .playlist-info {
        position: relative;
        display: grid;
        grid-template-columns: 300px 1fr;
        gap: 20px;
        isolation: isolate;
        padding: 20px;

        .playlist-picture {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 10px;
            overflow: hidden;
            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .icon {
                @include flex-center;
                height: 100%;
                width: 100%;
                background-color: $quinary-bg;

                svg {
                    width: 40%;
                    height: 40%;
                    color: $secondary-text;
                }
            }
        }

        .playlist-info-bg {
            z-index: -1;
            position: absolute;
            inset: 0;
            overflow: hidden;
            &.no-picture {
                background-color: $tertiary-bg;
            }
            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                filter: blur(20px) brightness(0.7);
            }
        }

        .playlist-info-content {
            display: flex;
            flex-direction: column;
            justify-content: center;

            .info-line {
                color: $secondary-text;
                font-size: 1rem;
                display: flex;
                align-items: center;
                gap: 5px;
                .value {
                    color: $primary-text;
                }
                .dot {
                    width: 3px;
                    height: 3px;
                    border-radius: 50%;
                    background-color: $secondary-text;
                }
            }
            .playlist-name {
                --font-size: 4rem;
                line-height: calc(var(--font-size) * 1.1);
                font-size: var(--font-size);
                font-weight: 700;
                text-transform: uppercase;
            }
        }
    }
    .playlist-tracks {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }
}
</style>
