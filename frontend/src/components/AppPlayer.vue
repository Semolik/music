<template>
    <div class="app-player-wrapper">
        <div class="app-player">
            <div class="player-buttons">
                <div class="player-button">
                    <FontAwesomeIcon icon="fa-backward" />
                </div>
                <div class="player-button" @click="togglePlaying">
                    <FontAwesomeIcon :icon="playing ? 'fa-pause' : 'fa-play'" />
                </div>
                <div class="player-button">
                    <FontAwesomeIcon icon="fa-forward" />
                </div>
            </div>
            <div class="column">
                <div class="info"></div>
                <div class="controls">
                    <div class="total">
                        <span style="font-weight: 700;">{{ _sToMs(seek) }} / {{ _sToMs(duration) }}</span>
                        <span style="font-weight: 700;">{{ curProgress }}%</span>
                    </div>
                    <div class="operatorButton">
                        <span class="iconfont icon-playcircle-fill" @click="togglePlayback" v-if="!playing">play</span>
                        <span class="iconfont icon-pausecircle-fill" @click="togglePlayback" v-else>pause</span>
                        <span class="iconfont icon-stopcircle-fill" @click="stop"></span>
                        <span class="iconfont icon-notificationfill" @click="handleToggleMute" v-if="isMute"></span>
                        <span class="iconfont icon-notificationforbidfill" @click="handleToggleMute" v-else></span>
                        <span class="iconfont icon-roundaddfill" @click="handleSetVolume(true)"></span>
                        <span class="iconfont icon-subtract_fill" @click="handleSetVolume(false)"></span>
                        <span class="iconfont icon-speed-2 rate" @click="handleSetRate" v-if="rate === 0.9"></span>
                        <span class="iconfont icon-speed-1 rate" @click="handleSetRate" v-if="rate === 1"></span>
                        <span class="iconfont icon-speed- rate" @click="handleSetRate" v-if="rate === 1.2"></span>
                    </div>
                    <div class="slider" ref="slider" @click="handleModifyProgress">
                        <div class="progressInfo"></div>
                        <div class="process" :style="{ width: pWidth }"></div>
                        <div class="thunk" ref="trunk" :style="{ left }">
                            <div class="block"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <audio controls ref="player" @play="playing = true" @loadstart="loading = true" @canplay="loading = false"
            @pause="playing = false" preload="auto"></audio>
    </div>
</template>
<script>

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlay, faPause, faForward, faBackward } from '@fortawesome/free-solid-svg-icons';
library.add(faPlay, faPause, faForward, faBackward);
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
            totalWidth: 500
        }
    },
    watch: {
        currentTrack() {
            if (!this.currentTrack) return
            var player = this.$refs.player;
            if (!player) return
            var url = this.currentTrack.url;
            if (player.src !== url) {
                player.src = url;
                player.load();
            }
            this.togglePlayer(this.playing);
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
    padding: 0px 5px;
    bottom: 10px;
    display: flex;
    width: min(1200px, 100%);

    audio {
        display: none;
    }

    .app-player {
        background-color: var(--color-background-mute);
        padding: 10px;
        width: 100%;
        border-radius: 20px;
        display: flex;

        .player-buttons {
            display: flex;
            gap: 5px;

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

                &:hover {
                    background-color: var(--color-background-mute-3);
                }
            }
        }
    }
}
</style>