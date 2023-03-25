<template>
    <html class="dark">
        <el-date-picker
            v-model="modelValueLocal"
            type="datetimerange"
            start-placeholder="Дата открытия"
            end-placeholder="Дата закрытия"
        />
    </html>
</template>
<script setup>
const { modelValue } = defineProps({
    modelValue: {
        type: Array,
        required: true,
    },
});
const emit = defineEmits(["modelValue"]);
const modelValueLocal = ref(modelValue);
watch(modelValueLocal, (newVal) => {
    emit("modelValue", newVal);
});
</script>
<style lang="scss">
@import url(element-plus/theme-chalk/dark/css-vars.css);
.el-date-editor {
    --el-date-editor-width: 100%;
    --el-input-height: 100%;
}
</style>
