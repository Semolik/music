import { defineStore } from 'pinia';
import { HTTP } from '../http-common.vue';

export const usePlayerStore = defineStore({
    id: 'player',
    state: () => ({
        tracks: [],
        currentTrackIndex: null,
        playing: false,
        player: null,
        playerMounted: false,
    }),
    getters: {
        currentTrack() {
            if (this.currentTrackIndex === null) return;
            return this.tracks[this.currentTrackIndex];
        },
        tracksIds() {
            return this.tracks.map(track => track.id)
        }
    },
    actions: {
        async getTrack(id) {
            var index = this.tracksIds.indexOf(id);
            if (index >= 0) {
                return index
            }
            try {
                const response = await HTTP.get('track', { params: { id: id } });
                return this.tracks.push(response.data) - 1;
            } catch (error) {
                return;
            }
        },
        async play(id) {
            if (this.currentTrack && this.currentTrack.id === id) {
                if (this.playing) {
                    this.player.pause();
                } else {
                    this.player.play();
                }
                return
            }



            this.currentTrackIndex = await this.getTrack(id);
            if (this.player) {
                // this.player.stop();
            }
        },
    }
});
