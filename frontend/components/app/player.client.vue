<template>
    <div class="app-player" v-show="playerStore.current_track_index !== null">
        <div
            class="primary-text text-center p-1"
            v-if="playerStore.currentTrack"
        >
            {{ playerStore.currentTrack?.name }} -
            {{ playerStore.currentTrack?.musician?.name }}
        </div>
        <AudioPlayer
            ref="player"
            :audio-list="listUrls"
            theme-color="hwb(153 26% 28%)"
            @pause="setPause(true)"
            @play="setPause(false)"
            @ended="playerStore.nextTrack()"
            :show-playback-rate="false"
        />
    </div>
</template>
<script setup>
import AudioPlayer from "@liripeng/vue-audio-player";
import { usePlayerStore } from "@/stores/player";
import { storeToRefs } from "pinia";
const playerStore = usePlayerStore();
const { listUrls, player, paused } = storeToRefs(playerStore);
const setting_pause = ref(false);
const setPause = (value) => {
    setting_pause.value = true;
    paused.value = value;
    setting_pause.value = false;
};
watch(paused, (newVal) => {
    if (!setting_pause.value) {
        if (newVal) {
            player.value.pause();
        } else {
            player.value.play();
        }
    }
});
</script>
<style lang="scss">
.app-player {
    .audio-player {
        padding-inline: 20px;
        .audio__btn-wrap {
            padding-top: 10px;
        }
    }
}
</style>
