<template>
    {{ playerStore.listUrls }}
    <div class="player">
        <AudioPlayer ref="player" :audio-list="listUrls" />
    </div>
</template>
<script setup>
import AudioPlayer from "@liripeng/vue-audio-player";
import { usePlayerStore } from "@/stores/player";
import { storeToRefs } from "pinia";
const playerStore = usePlayerStore();
const { listUrls, player } = storeToRefs(playerStore);
</script>
