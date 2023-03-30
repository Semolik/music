<template>
    <el-switch
        :model-value="modelValue"
        @update:modelValue="emit('update:modelValue', $event)"
    />
</template>
<script setup>
const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);
</script>
<style scoped lang="scss">
.el-switch {
    --el-switch-off-color: #{$primary-bg};
    --el-switch-on-color: #{$accent};
    --el-color-primary: #{$accent};
    --el-text-color-primary: #{$secondary-text};
}
</style>
