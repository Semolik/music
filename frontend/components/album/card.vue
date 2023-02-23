<template>
    <card-min v-bind="props" v-if="min">
        <template #content>
            <span>{{ album.name }}</span>
            <div class="flex gap-3px items-center secondary-text text-sm">
                <span>{{ album.musician.name }}</span>
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
    <card v-bind="props" v-else />
</template>
<script setup>
const runtimeConfig = useRuntimeConfig();
const { album } = defineProps({
    album: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
});

const props = reactive({
    text: album.name,
    picture: album.picture,
    icon: runtimeConfig.public.albumIcon,
});
</script>
