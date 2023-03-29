<template>
    <div class="index-selection">
        <div class="selection-head">
            <div class="selection-title">
                {{ title }}
            </div>
            <div class="selection-description" v-if="description">
                {{ description }}
            </div>
        </div>
        <div class="selection-content">
            <slot />
        </div>
    </div>
</template>
<script setup>
const { title, description } = defineProps({
    title: {
        type: String,
        required: true,
    },
    description: {
        type: String,
        required: false,
    },
});
</script>
<style lang="scss" scoped>
.index-selection {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    .selection-head {
        display: flex;
        flex-direction: column;

        .selection-title {
            font-size: 24px;
            font-weight: 600;
            color: $primary-text;
        }
        .selection-description {
            font-size: 14px;
            font-weight: 400;
            color: $secondary-text;
        }
    }

    .selection-content {
        display: flex;
        flex-direction: column;
        gap: 10px;
        height: 100%;
    }
}
</style>
