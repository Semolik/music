<template>
    <div class="track" @mouseover="hovered = true" @mouseleave="hovered = false" @click="OnClickTrack">
        <AlbumPicture :play-icon="isPlaying || hovered" :paused="playing" :src="trackData.picture" off-hover />
        <div class="track-info-wrapper">
            <div class="track-info">
                <div class="name">{{ trackData.name }}</div>
                <router-link to="/" class="musician">{{ musicianData.name }}</router-link>
            </div>
        </div>
        <div class="track-duration">{{ duration }}</div>
    </div>
</template>
<script>
import AlbumPicture from './AlbumPicture.vue';
import moment from 'moment';
import { usePlayerStore } from '../stores/player';
import { storeToRefs } from 'pinia';
export default {
    props: {
        trackData: Object,
        musicianData: Object,
    },
    setup() {
        const { currentTrack, playing } = storeToRefs(usePlayerStore());
        const playerStore = usePlayerStore();
        return { currentTrack, playerStore, playing };
    },
    data() {
        return {
            hovered: false,
        }
    },
    components: { AlbumPicture },
    computed: {
        duration() {
            const time = moment.utc(this.trackData.duration * 1000);
            if (time.hours() > 1) {
                return time.format('HH:mm:ss')
            }
            return time.format('mm:ss')
        },
        isPlaying() {
            if (!this.currentTrack) return
            return this.currentTrack.id === this.trackData.id;
        }
    },
    methods: {
        OnClickTrack() {
            this.playerStore.play(this.trackData.id)
        }
    }
}
</script>
<style lang="scss">
.track {
    background-color: var(--color-background-mute-3);
    padding: 8px;
    border-radius: 10px;
    display: grid;
    grid-template-columns: 50px 1fr min-content;
    align-items: center;
    gap: 10px;
    cursor: pointer;


    .picture {
        --picture-border-radius: 5px;
        --picture-color: var(--color-background-mute-4);
        --svg-size: 22px;
        --svg-color: var(--vt-c-white-200)
    }

    .track-info-wrapper {
        display: flex;
        align-items: center;

        .track-info {

            .musician {
                color: var(--color-header-text);
                text-decoration: none;

                &:hover {
                    color: var(--yellow);
                }
            }

        }
    }

    .track-duration {
        color: var(--color-header-text);
        padding: 0px 10px;
    }

}
</style>