import { defineStore } from "pinia";

export const usePlayerStore = defineStore({
    id: "player",
    state: () => ({
        tracks: [],
        current_track_index: null,
        player: null,
    }),
    actions: {
        setTracks(tracks, currentTrack) {
            this.tracks = tracks;
            this.current_track_index = this.tracks.findIndex(
                (track) => track.id === currentTrack.id
            );
        },
        playCurrentTrack() {
            this.player.currentPlayIndex = this.current_track_index || 0;
            this.player.play();
        },
    },
    getters: {
        listUrls() {
            return this.tracks.map((track) => track.url);
        },
    },
});
