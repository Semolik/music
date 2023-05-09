<template>
    <div class="player">
        <AudioPlayer ref="player" :audio-list="playerStore.listUrls" />
    </div>
</template>
<script setup>
const player = ref(null);
import AudioPlayer from "@liripeng/vue-audio-player";
import { usePlayerStore } from "@/stores/player";

const playerStore = usePlayerStore();
</script>
<style lang="scss" scoped>

</style>
