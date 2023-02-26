<template>
    <el-input v-bind="$attrs" v-model="value" />
</template>
<script setup>
const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    },
    height: {
        type: String,
        default: "40px",
    },
    append: {
        type: String,
        default: "",
    },
});
const height = ref(props.height);
const value = ref(props.modelValue);
const emit = defineEmits(["update:modelValue"]);
watch(value, (val) => {
    emit("update:modelValue", val);
});
</script>
<style lang="scss">
.el-input {
    --el-input-bg-color: #{$secondary-bg};
    --el-fill-color-blank: var (--el-input-bg-color);
    --el-input-border-color: #{$quaternary-text};
    --el-input-hover-border-color: #{$tertiary-text};
    --el-input-focus-border-color: #{$accent};
    --el-input-text-color: #{$primary-text};
    --el-input-height: v-bind(height);
    // --el-input-border-radius: 0px 4px 4px 0px;
}
</style>
