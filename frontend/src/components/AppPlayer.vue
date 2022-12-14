<template>
    <div class="app-player-wrapper">
        <div class="app-player">
            <div class="slider" ref="slider" @click="handleModifyProgress">
                <div class="progressInfo"></div>
                <div class="process" :style="{ width: pWidth }"></div>
                <div class="thunk" ref="trunk" :style="{ left }">
                    <div class="block"></div>
                </div>
            </div>
            <div class="player-buttons">
                <div class="player-button">
                    <FontAwesomeIcon icon="fa-backward" />
                </div>
                <div class="player-button" @click="togglePlayback">
                    <FontAwesomeIcon :icon="playing ? 'fa-pause' : 'fa-play'" />
                </div>
                <div class="player-button" @click="playNext">
                    <FontAwesomeIcon icon="fa-forward" />
                </div>
            </div>
            <div class="column">
                <div class="info">
                    <div class="track-info">
                        <div class="name">{{ currentTrack.name }}</div>
                        <router-link to="/" class="artist">{{ currentTrack.album.musician.name }}</router-link>
                    </div>
                    <div class="progress">
                        {{ _sToMs(seek) }} / {{ _sToMs(duration) }}
                    </div>
                </div>
                <!-- <div class="controls">
                    <div class="total">
                       
                        <span style="font-weight: 700;">{{ curProgress }}%</span>
                    </div>
                    <div class="operatorButton">
                        <span class="iconfont icon-stopcircle-fill" @click="stop"></span>
                        <span class="iconfont icon-notificationfill" @click="handleToggleMute" v-if="isMute"></span>
                        <span class="iconfont icon-notificationforbidfill" @click="handleToggleMute" v-else></span>
                        <span class="iconfont icon-roundaddfill" @click="handleSetVolume(true)"></span>
                        <span class="iconfont icon-subtract_fill" @click="handleSetVolume(false)"></span>
                        <span class="iconfont icon-speed-2 rate" @click="handleSetRate" v-if="rate === 0.9"></span>
                        <span class="iconfont icon-speed-1 rate" @click="handleSetRate" v-if="rate === 1"></span>
                        <span class="iconfont icon-speed- rate" @click="handleSetRate" v-if="rate === 1.2"></span>
                    </div>

                </div> -->
            </div>
            <div class="player-buttons">
                <div :class="['player-button', 'like', { active: currentTrack?.liked }]"
                    @click="likeTrack(currentTrackId)">
                    <FontAwesomeIcon icon="fa-heart" />
                </div>
                <div class="player-button" @click="toggleVolumeBlock">
                    <FontAwesomeIcon :icon="iconVolumeName" />
                </div>
                <div class="volume-block" v-if="volumeBlockOpened">
                    <input type="range" :min="min" :max="max" v-model="sliderVolume">
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlay, faPause, faForward, faBackward, faHeart, faVolumeOff, faVolumeLow, faVolumeHigh } from '@fortawesome/free-solid-svg-icons';
library.add(faPlay, faPause, faForward, faBackward, faHeart, faVolumeOff, faVolumeLow, faVolumeHigh);
import { usePlayerStore } from '../stores/player';
import { storeToRefs } from 'pinia';
import Audio from '../mixins/audio';
export default {
    mixins: [Audio],
    components: { FontAwesomeIcon },
    data() {
        return {
            min: 0,
            max: 100,
            slider: null,
            thunk: null,
            per: 0,
            rate: 1,
            isMute: true,
            curVolume: 0.5,
            sliderVolume: 50,
            totalWidth: 500,
            volumeBlockOpened: false,
        }
    },
    setup() {
        const { playing, currentTrack, currentTrackId } = storeToRefs(usePlayerStore());
        const { likeTrack, playNext } = usePlayerStore();
        return {
            playing, currentTrack, currentTrackId, likeTrack, playNext
        }
    },
    watch: {
        currentTrack(value) {
            if (!value) return
            var player = this.$refs.player;
            if (!player) return
            var url = value.url;
            if (player.src !== url) {
                player.src = url;
                player.load();
            }
            this.togglePlayer(this.playing);
        },
        sliderVolume(value) {
            this.curVolume = value / 100;
            this.setVolume(this.curVolume);
        },
        playing(value) {
            this.togglePlayer(value);
        },
        curProgress(v) {
            if (!document.onmouseup) {
                this.per = v;
            }
        }
    },
    methods: {
        openVolumeBlock() {
            this.volumeBlockOpened = true;
        },
        closeVolumeBlock() {
            this.volumeBlockOpened = false;
        },
        toggleVolumeBlock() {
            this.volumeBlockOpened = !this.volumeBlockOpened;
        },
        togglePlayer(play) {
            var player = this.$refs.player;
            if (!player) return
            if (play) {
                player.play()
            } else {
                player.pause()
            }
        },
        handleModifyProgress(e) {
            if (e.target.className === 'slider' || e.target.className === 'process') {
                let scale = e.offsetX / this.slider.offsetWidth;
                this.setProgress(scale);
            }
        },
        handleSetRate() {
            if (this.rate === 1) {
                this.rate = 0.9;
                this.setRate(this.rate);
            } else if (this.rate === 0.9) {
                this.rate = 1.2;
                this.setRate(this.rate);
            } else {
                this.rate = 1;
                this.setRate(this.rate);
            }
        },
        handleToggleMute() {
            this.isMute ? this.isMute = false : this.isMute = true;
            this.toggleMute();
        },
        handleSetVolume(flag) {
            flag ? this.curVolume += 0.1 : this.curVolume -= 0.1;
            this.curVolume > 1 ? this.curVolume = 1 : this.curVolume < 0 ? this.curVolume = 0 : '';
            this.setVolume(this.curVolume);
        },
        _sToMs(s) {
            if (typeof s !== 'number') return '00' + ':' + '00'
            s = parseInt(s);
            let h;
            h = Math.floor(s / 60);
            s = s % 60;
            h += '';
            s += '';
            h = (h.length == 1) ? '0' + h : h;
            s = (s.length == 1) ? '0' + s : s;
            return h + ':' + s;
        }
    },
    computed: {
        iconVolumeName() {
            var volume = Number(this.sliderVolume);
            if (volume === 0) {
                return 'fa-volume-off'
            }
            if (volume <= 50) {
                return 'fa-volume-low'
            }
            if (volume > 50) {
                return 'fa-volume-high'
            }
        },
        curProgress() {
            let curProgress = ((Math.round((this.progress * 10000))) / 100.00).toFixed(2);
            return curProgress;
        },
        scale() {
            let scale = (this.per - this.min) / (this.max - this.min);
            return scale;
        },
        pWidth() {
            if (this.slider) {
                return this.slider.offsetWidth * this.scale + 'px';
            } else {
                return 0 + 'px'
            }
        },
        left() {
            if (this.slider) {
                return this.slider.offsetWidth * this.scale - this.thunk.offsetWidth / 2 + 'px';
            } else {
                return 0 + 'px'
            }
        }
    },
    mounted() {
        if (this.width && typeof this.width === 'number') {
            this.totalWidth = this.width + 'px';
        }
        this.setVolume(this.curVolume);
        this.slider = this.$refs.slider;
        this.thunk = this.$refs.trunk;
        this.thunk.onmousedown = e => {
            let pWidth = parseInt(this.pWidth);
            let disX = e.clientX;
            document.onmousemove = e => {
                let newWidth = e.clientX - disX + pWidth;
                let scale = newWidth / this.slider.offsetWidth;
                this.per = Math.ceil((this.max - this.min) * scale + this.min);
                this.per = Math.max(this.per, this.min);
                this.per = Math.min(this.per, this.max);
            }
            document.onmouseup = () => {
                document.onmousemove = document.onmouseup = null;
                this.setProgress(this.scale);
            }
            return false;
        }
    },
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.app-player-wrapper {
    position: absolute;
    bottom: 0px;
    display: flex;
    width: min(1200px, 100%);

    audio {
        display: none;
    }

    .app-player {
        background-color: var(--color-background-mute);
        padding: 10px;
        width: 100%;
        display: flex;
        gap: 10px;
        position: relative;

        .slider {
            height: 10px;
            position: absolute;
            border: 0;
            width: 100%;
            left: 0;
            bottom: 100%;
            isolation: isolate;
            overflow: hidden;
            cursor: pointer;
            border-radius: 5px 5px 0px 0px;

            .progressInfo {
                position: absolute;
                inset: 0;
                background-color: var(--color-background-mute-3);
            }

            .process {
                position: absolute;
                inset: 0;
                background-color: var(--color-background-mute-5);
            }

            .thunk {
                position: absolute;
                inset: 0;
                z-index: 2;
            }
        }

        .column {
            flex-grow: 1;
            display: flex;

            .info {
                display: flex;
                align-items: center;
                width: 100%;

                .track-info {
                    display: flex;
                    flex-direction: column;
                }

                .progress {
                    margin-left: auto;
                    color: var(--color-header-text);
                }

                .artist {
                    font-size: 0.9em;
                    color: var(--color-header-text);
                    text-decoration: none;

                    &:hover {
                        color: var(--yellow);
                    }
                }
            }
        }

        .player-buttons {
            display: flex;
            gap: 5px;
            position: relative;

            .volume-block {
                position: absolute;
                background-color: var(--color-background-mute);
                bottom: calc(100% + 25px);
                right: -10px;
                border-radius: 5px;
                padding: 0px 10px;
                @include helpers.flex-center;

                input[type=range] {

                    height: 36px;
                    width: 100px;
                    border-radius: 3px;
                    background: var(--color-background-mute-3);
                    cursor: pointer;
                }
            }

            .player-button {
                @include helpers.flex-center;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background-color: var(--color-background-mute-2);
                cursor: pointer;

                svg {
                    color: var(--color-header-text);
                }

                &.like.active svg {
                    color: var(--red-0)
                }

                &:hover {
                    background-color: var(--color-background-mute-3);
                }
            }
        }
    }
}
</style>