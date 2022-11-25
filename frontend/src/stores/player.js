import { defineStore } from 'pinia';
import { HTTP } from '../http-common.vue';

export const usePlayerStore = defineStore({
    id: 'player',
    state: () => ({
        tracks: [],
        geted_albums: [],
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
        },
        currentTrackId() {
            if (!this.currentTrack) return
            return this.currentTrack.id
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
        async getAlbum(track_id, album_id) {
            try {
                var saved_album = this.geted_albums.find((album) => album.id === album_id);
                if (saved_album) {
                    var tracks = this.tracks.slice(saved_album.start, saved_album.end);
                    var startIndex = saved_album.start;
                } else {
                    const response = await HTTP.get('album', { params: { id: album_id } });
                    let startIndex = this.tracks.length;
                    var tracks = response.data.tracks;
                    this.geted_albums.push({ id: album_id, start: startIndex, end: startIndex + tracks.length - 1 });
                    this.tracks.push(...tracks.map(track => {
                        track['album'] = {
                            musician: response.data.musician
                        };
                        return track
                    }));
                }
                var startIndexInAlbum = tracks.map(track => track.id).indexOf(track_id);
                return startIndex + (startIndexInAlbum > 0 ? startIndexInAlbum : 0);
            } catch (error) {
                return;
            }
        },
        async play(id, album_id = null) {
            if (this.currentTrack && this.currentTrack.id === id) {
                if (this.playing) {
                    this.player.pause();
                } else {
                    this.player.play();
                }
                return
            }
            if (album_id) {
                this.currentTrackIndex = await this.getAlbum(id, album_id);
            } else {
                this.currentTrackIndex = await this.getTrack(id);
            }
        },
        likeTrack(track_id) {
            if (!this.currentTrack) return
            HTTP.post('like', null, { params: { track_id: track_id } })
                .then(response => {
                    this.tracks[this.currentTrackIndex].liked = response.data.liked;
                }).catch(error => {
                    console.log('Произошла ошибка при отправке запроса на добавление трека в избранное.')
                })

        }
    }
});
