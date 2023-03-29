<template>
    <Selection title="Чарт">
        <div class="tracks-container">
            <TrackCard v-for="track in tracks" :key="track.id" :track="track" />
        </div>
    </Selection>
</template>
<script setup>
import { Service } from "~~/client";
const tracks = await Service.getPopularTracksMonthApiV1TracksPopularMonthGet();
</script>
<style lang="scss" scoped>
.tracks-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 10px;
}
</style>
