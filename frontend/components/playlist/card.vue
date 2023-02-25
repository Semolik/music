<template>
    <card-min v-bind="props" v-if="min">
        <template #content>
            <span>{{ playlist.name }}</span>
            <div class="flex gap-3px items-center secondary-text text-sm">
                <span>Количество треков: {{ playlist.tracks_count }}</span>
            </div>
        </template>
        <template #card-end>
            <div class="flex justify-center items-center pr-4 secondary-text">
                <Icon name="material-symbols:arrow-forward-ios" />
            </div>
        </template>
    </card-min>
    <card v-bind="props" v-else>
        <div class="flex flex-col grow">
            <span class="font-medium">{{ playlist.name }}</span>
            <div class="secondary-text text-sm flex-wrap flex items-center">
                <span> Количество треков: {{ playlist.tracks_count }}</span>
            </div>
        </div>
    </card>
</template>
<script setup>
const runtimeConfig = useRuntimeConfig();
const { playlist } = defineProps({
    playlist: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
});

const props = reactive({
    picture: playlist.picture,
    icon: runtimeConfig.public.playlistIcon,
});
</script>
