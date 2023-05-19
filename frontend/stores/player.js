import { defineStore } from "pinia";

export const usePlayerStore = defineStore({
    id: "player",
    state: () => ({
        tracks: [],
        current_track_index: null,
        player: null,
        paused: true,
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
        toggleCurrentTrack() {
            if (this.paused) {
                this.playCurrentTrack();
            } else {
                this.player.pause();
            }
        },
        nextTrack() {
            this.current_track_index++;
            if (this.current_track_index >= this.tracks.length) {
                this.paused = true;
                this.current_track_index = null;
                this.tracks = [];
                return;
            }
            this.playCurrentTrack();
        },
    },
    getters: {
        listUrls() {
            return this.tracks.map((track) => track.url);
        },
        currentTrack() {
            if (!this.tracks.length) return null;
            return this.tracks[this.current_track_index];
        },
    },
});
