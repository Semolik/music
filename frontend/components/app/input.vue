<template>
    <div :class="['app-input', { 'error-border': error }]">
        <label v-if="label" class="app-input__label">{{ label }}</label>
        <el-input
            v-bind="$attrs"
            v-model="value"
            :class="{
                resize: resize,
            }"
        >
            <template #suffix>
                <span
                    :class="[
                        'el-input__count',
                        { disabled: !showWordLimit || !value },
                    ]"
                    v-if="showWordLimit"
                >
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
    </div>
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
    resizeOnFocus: {
        type: Boolean,
        default: true,
    },
    typingPlaceholderValues: {
        type: Array,
        default: () => [],
    },
    label: {
        type: String,
        default: "",
    },
    error: {
        type: Boolean,
        default: false,
    },
});
const height = ref(props.height);
const value = ref(props.modelValue);
const showWordLimit = ref(props.showWordLimit);
const emit = defineEmits(["update:modelValue"]);
const resize = ref(false);
if (props.resizeOnFocus) {
    const viewport = useViewport();

    watch(
        viewport.breakpoint,
        () => {
            if (viewport.isGreaterOrEquals("lg")) {
                resize.value = false;
            } else {
                resize.value = true;
            }
        },
        { immediate: true }
    );
}
watch(value, (val) => {
    if (props.maxLength && val.length > props.maxLength) {
        value.value = val.slice(0, props.maxLength);
    }
    emit("update:modelValue", val);
});
</script>
<style lang="scss">
.app-input {
    display: flex;
    flex-direction: column;
    gap: 2px;
    width: 100%;
    height: min-content;

    .app-input__label {
        padding-left: 5px;
        font-size: 14px;
        color: var(--app-input-label, #{$secondary-text});
    }

    &.error-border {
        --app-input-border: var(--app-input-error-border, #{$accent-red});
        --app-input-hover-border: var(--app-input-error-border, #{$accent-red});
        --app-input-focus-border: var(--app-input-error-border, #{$accent-red});
    }

    .el-input {
        flex-grow: 1;
        --el-input-bg-color: var(--app-input-bg, #{$secondary-bg});
        --el-fill-color-blank: var(--app-input-bg, #{$secondary-bg});
        --el-input-border-color: var(--app-input-border, #{$quaternary-text});
        --el-input-hover-border-color: var(
            --app-input-hover-border,
            #{$tertiary-text}
        );
        --el-input-focus-border-color: var(
            --app-input-focus-border,
            #{$accent}
        );
        --el-input-text-color: var(--app-input-text, #{$primary-text});
        --el-input-border-radius: var(--app-input-border-radius, 10px);
        --el-input-height: v-bind(height);

        &.resize {
            @media screen and (-webkit-min-device-pixel-ratio: 0) {
                select:focus,
                textarea:focus,
                input:focus {
                    font-size: 16px;
                }
            }
        }

        .el-input__count {
            opacity: 1;
            user-select: none;
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
}
</style>
