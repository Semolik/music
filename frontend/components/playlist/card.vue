<template>
    <card-min v-bind="props" v-if="min">
        <template #content>
            <span>{{ playlist.name }}</span>
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
    text: playlist.name,
    picture: playlist.picture,
    icon: runtimeConfig.public.albumIcon,
});
</script>
