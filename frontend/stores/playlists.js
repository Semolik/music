import { defineStore } from "pinia";
import { Service } from "@/client";
export const usePlaylistsStore = defineStore({
    id: "playlists",
    state: () => ({
        playlists_cache: [],
        playlists_fetched: false,
    }),
    getters: {
        playlists() {
            if (this.playlists_fetched) {
                return this.playlists_cache;
            }
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
            this.playlists_cache.push(playlist);
        },
        async fetchPlaylists() {
            this.playlists_cache = [
                ...this.playlists_cache,
                ...(await Service.getMyPlaylistsApiV1PlaylistsGet()),
            ];
            this.playlists_fetched = true;
        },
        async addTrackToPlaylist({ playlistId, trackId }) {
            await Service.addTrackToPlaylistApiV1PlaylistsPlaylistIdTrackTrackIdPost(
                trackId,
                playlistId
            );
            this.playlists_cache = this.playlists_cache.map((playlist) => {
                if (playlist.id === playlistId) {
                    playlist.tracks_count += 1;
                }
                return playlist;
            });
        },
        async removeTrackFromPlaylist({ playlistId, trackId }) {
            await Service.deleteTrackFromPlaylistApiV1PlaylistsPlaylistIdTrackTrackIdDelete(
                trackId,
                playlistId
            );
            this.playlists_cache = this.playlists_cache.map((playlist) => {
                if (playlist.id === playlistId) {
                    playlist.tracks_count -= 1;
                }
                return playlist;
            });
        },
        addPlaylistToCache(playlist) {
            this.playlists_cache.push(playlist);
        },
    },
});
