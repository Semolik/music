import { defineStore } from 'pinia';


export const usePlayerStore = defineStore({
    id: 'player',
    state: () => ({
        tracks: [],
        currentTrackIndex: null,
    }),
    getters: {
        currentTrack() {
            if (!this.currentTrackIndex) return;
            return tracks[this.currentTrackIndex];
        },
    },
    actions: {
        // getTrack()
    }
});
