<template>
    <card-min v-bind="props" v-if="min" @click="goToAlbum">
        <template #content>
            <span>{{ album.name }}</span>
            <div class="flex gap-3px items-center secondary-text text-sm">
                <span>{{ musicianName }}</span>
                <Icon name="ci:dot-02-s" />
                <span>{{ album.year }}</span>
            </div>
        </template>
        <template #card-end>
            <div class="flex justify-center items-center pr-4 secondary-text">
                <Icon name="material-symbols:arrow-forward-ios" />
            </div>
        </template>
    </card-min>
    <card v-bind="props" v-else @picture-click="goToAlbum" :is-link="isLink">
        <div class="flex flex-col grow">
            <span class="font-medium primary-text">{{ album.name }}</span>
            <div class="secondary-text text-sm flex-wrap flex items-center">
                <span> {{ musicianName }}</span>
                <Icon name="ci:dot-02-s" />
                <span>{{ album.year }}</span>
            </div>
        </div>
    </card>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { album, musicianInfo, disableLink, isLink } = defineProps({
    album: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
    musicianInfo: {
        type: Object,
        required: false,
    },
    disableLink: {
        type: Boolean,
        default: false,
    },
    isLink: {
        type: Boolean,
        default: false,
    },
});
const musicianName = computed(() => {
    if (musicianInfo) {
        return musicianInfo.name;
    }
    return album.musician.name;
});
const props = reactive({
    picture: album.picture,
    icon: IconsNames.albumIcon,
});
const router = useRouter();
const goToAlbum = () => {
    if (disableLink) {
        return;
    }
    router.push({
        name: "album-id",
        params: {
            id: album.id,
            albumId: album.id,
        },
    });
};
</script>
