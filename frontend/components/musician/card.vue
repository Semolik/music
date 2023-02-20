<template>
    <card-min v-bind="props" v-if="min">
        <template #content>
            <span>{{ musician.name }}</span>
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
const { musician } = defineProps({
    musician: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
});
const props = reactive({
    text: musician.name,
    picture: musician.picture,
    icon: runtimeConfig.public.musicianIcon,
});
</script>
