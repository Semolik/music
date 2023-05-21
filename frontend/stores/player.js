import { defineStore } from "pinia";
import { Service } from "~/client";
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
            this.current_track_index = tracks.findIndex(
                (track) => track.id === currentTrack.id
            );
            this.tracks = tracks;
        },
        playCurrentTrack() {
            if (!this.player) {
                this.player.play();
            }
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
        updateTrack(track) {
            const trackIndex = this.tracks.findIndex((t) => t.id === track.id);
            if (trackIndex === -1) return;
            this.tracks[trackIndex] = track;
        },
        async toggleLike() {
            try {
                this.tracks[this.current_track_index].liked =
                    await Service.likeTrackApiV1TracksTrackIdLikePut(
                        this.tracks[this.current_track_index].id
                    );
            } catch (error) {
                console.log(error);
            }
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
        isLastTrack() {
            return this.current_track_index === this.tracks.length - 1;
        },
        isFirstTrack() {
            return this.current_track_index === 0;
        },
    },
});
