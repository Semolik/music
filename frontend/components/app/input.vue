<template>
    <el-input v-bind="$attrs" v-model="value">
        <template #suffix v-if="props.showWordLimit">
            <span :class="['el-input__count', { disabled: !value }]">
                <span class="el-input__count-inner">
                    <span
                        :class="[
                            'current-length',
                            { warning: value.length < props.minLength },
                        ]"
                        >{{ value.length }}</span
                    >
                    /
                    <span class="max-length">{{ maxLength }}</span>
                </span>
            </span>
        </template>
    </el-input>
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
    showWordLimit: {
        type: Boolean,
        default: false,
    },
    minLength: {
        type: Number,
        default: 0,
    },
    maxLength: {
        type: Number,
        default: 0,
    },
});
const height = ref(props.height);
const value = ref(props.modelValue);
const emit = defineEmits(["update:modelValue"]);
watch(value, (val) => {
    if (props.maxLength && val.length > props.maxLength) {
        value.value = val.slice(0, props.maxLength);
    }
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

    .el-input__count {
        opacity: 1;
        &.disabled {
            opacity: 0;
        }
        .el-input__count-inner {
            .current-length {
                &.warning {
                    color: #{$accent-red};
                }
            }
        }
    }
}
</style>
