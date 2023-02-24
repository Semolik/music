<template>
    <el-input placeholder="Please input" v-bind="$attrs" v-model="value" />
</template>
<script setup>
const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    },
});
const value = ref(props.modelValue);
const emit = defineEmits(["update:modelValue"]);
watch(value, (val) => {
    emit("update:modelValue", val);
});
</script>
<style lang="scss">
.el-input {
    --el-input-bg-color: var(--app-input-bg-color, #{$tertiary-bg});
    --el-input-border-color: transparent;
    --el-input-hover-border-color: transparent;

    --el-input-focus-border-color: transparent;
}
</style>
