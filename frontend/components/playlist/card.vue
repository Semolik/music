<template>
    <card-min v-bind="props" v-if="min" @click="emit('card-click')">
        <template #content>
            <span>{{ playlist.name }}</span>
            <div class="flex gap-3px items-center secondary-text text-sm">
                <span>Количество треков: {{ playlist.tracks_count }}</span>
            </div>
        </template>
        <template #card-end>
            <div
                class="flex justify-center items-center pr-4 secondary-text"
                v-if="!hideEndIcon"
            >
                <Icon name="material-symbols:arrow-forward-ios" />
            </div>
            <slot name="card-end" />
        </template>
    </card-min>
    <card v-bind="props" v-else @picture-click="emit('card-click')">
        <div class="flex flex-col grow">
            <span class="font-medium">{{ playlist.name }}</span>
            <div class="secondary-text text-sm flex-wrap flex items-center">
                <span> Количество треков: {{ playlist.tracks_count }}</span>
            </div>
        </div>
    </card>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const emit = defineEmits(["card-click"]);
const { playlist, min, hideEndIcon } = defineProps({
    playlist: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
    hideEndIcon: {
        type: Boolean,
        default: false,
    },
});

const props = reactive({
    picture: playlist.picture,
    icon: IconsNames.playlistIcon,
});
</script>
