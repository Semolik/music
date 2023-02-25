<template>
    <card-min v-bind="props">
        <template #content>
            <span>{{ track.album.musician.name }}</span>
        </template>
        <template #card-end>
            <div class="track-dots-button-container">
                <span>{{ duration }}</span>
                <div class="track-dots-button">
                    <Icon :name="dotsIcon" />
                </div>
            </div>
        </template>
    </card-min>
</template>
<script setup>
import moment from "moment";
const runtimeConfig = useRuntimeConfig();
const { dotsIcon } = runtimeConfig.public;
const { track } = defineProps({
    track: {
        type: Object,
        required: true,
    },
});
const duration = computed(() =>
    moment
        .utc(moment.duration(track.duration, "seconds").asMilliseconds())
        .format("mm:ss")
);
const props = reactive({
    picture: track.picture,
    icon: runtimeConfig.public.trackIcon,
});
</script>
<style lang="scss" scoped>
.track-dots-button-container {
    @include flex-center;
    color: $secondary-text;
    gap: 8px;
    padding-right: 0.5rem;
    .track-dots-button {
        border-radius: 50%;
        @include flex-center;

        height: min-content;
        padding: 8px;
        &:hover {
            background-color: $quaternary-bg;
        }
    }
}
</style>
