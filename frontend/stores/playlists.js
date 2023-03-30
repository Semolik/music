import { defineStore } from "pinia";
import { Service } from "@/client";
export const usePlaylistsStore = defineStore({
    id: "playlists",
    state: () => ({
        playlists_cache: null,
    }),
    getters: {
        playlists() {
            if (this.playlists_cache !== null) {
                return this.playlists_cache;
            }
            this.playlists_cache = [];
            this.fetchPlaylists();
            return this.playlists_cache;
        },
    },
    actions: {
        async createPlaylist({ name, trackIds, is_public }) {
            const playlist = await Service.createPlaylistApiV1PlaylistsPost({
                tracks_ids: trackIds,
                name: name,
                description: null,
                private: !is_public,
            });
            if (this.playlists_cache === null) {
                this.playlists_cache = [];
            }
            this.playlists_cache.push(playlist);
        },
        async fetchPlaylists() {
            this.playlists_cache =
                await Service.getMyPlaylistsApiV1PlaylistsGet();
        },
    },
});
