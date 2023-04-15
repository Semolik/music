<template>
    <card-min v-bind="props" v-if="min" @click="onCardClick">
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
    <card
        @click="onCardClick"
        v-bind="props"
        v-else
        :class="{ 'is-link': isLink }"
    >
        <template #picture v-if="playlist.private">
            <div class="private-icon">
                <Icon name="material-symbols:lock" />
            </div>
        </template>
        <div class="flex flex-col grow">
            <span
                class="primary-text font-medium text-ellipsis overflow-hidden"
                >{{ playlist.name }}</span
            >
            <div class="secondary-text text-sm flex-wrap flex items-center">
                <span>Количество треков: {{ playlist.tracks_count }}</span>
            </div>
        </div>
    </card>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";
const emit = defineEmits(["card-click"]);
const { playlist, min, hideEndIcon, isLink } = defineProps({
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
    isLink: {
        type: Boolean,
        default: false,
    },
});
const router = useRouter();
const onCardClick = () => {
    emit("card-click");
    if (isLink) {
        router.push({
            name: routesNames.playlistId,
            params: { id: playlist.id },
        });
    }
};
const props = reactive({
    picture: playlist.picture,
    icon: IconsNames.playlistIcon,
});
</script>
<style scoped lang="scss">
.private-icon {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: $secondary-bg;
    border-radius: 5px;

    svg {
        width: 30px;
        height: 30px;
        color: $secondary-text;
    }
}
.is-link {
    background-color: $secondary-bg;
    padding: 10px;
    border-radius: 10px;
    @include lg {
        &:hover {
            background-color: $secondary-bg-2;
        }
    }
}
</style>
