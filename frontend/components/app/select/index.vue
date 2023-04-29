<template>
    <div class="app-select">
        <div class="title">{{ title }}</div>
        <div class="values">
            <div
                :class="[
                    'value',
                    {
                        active: modelValue === value,
                    },
                ]"
                v-for="value in values"
                @click="() => emit('update:modelValue', value)"
            >
                {{ value }}
            </div>
        </div>
        <div v-if="disabled" class="disabled">
            <Icon name="material-symbols:lock" />
        </div>
    </div>
</template>
<script setup>
const { modelValue, values } = defineProps({
    modelValue: {
        type: [String, Number],
        required: true,
    },
    values: {
        type: Array,
        required: true,
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    title: {
        type: String,
        default: "",
    },
});

const emit = defineEmits(["update:modelValue"]);
</script>
<style scoped lang="scss">
.app-select {
    display: flex;
    flex-direction: column;
    gap: 5px;
    @include lg(true) {
        gap: 10px;
    }
    position: relative;
    .disabled {
        position: absolute;
        inset: -3px;
        border-radius: 10px;
        background-color: rgba(0, 0, 0, 0.5);
        @include flex-center;

        svg {
            width: 30px;
            height: 30px;
            color: $secondary-text;
        }
    }
    .title {
        font-size: 14px;
        color: $secondary-text;
    }
    .values {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        padding: 5px;
        background-color: var(--app-select-bg, $tertiary-bg);
        border-radius: 10px;
        @include lg(true) {
            padding: 0px;
            flex-direction: column;
            overflow: hidden;
            border-radius: 10px;
            gap: 0px;
        }
        .value {
            @include flex-center;
            height: 30px;
            border-radius: 5px;
            cursor: pointer;
            color: $secondary-text;
            user-select: none;
            flex-grow: 1;
            padding: 0 10px;
            text-align: center;
            @include lg(true) {
                border-radius: 0px;
                min-height: 40px;
            }
            &.active {
                background-color: $accent;
                color: $primary-bg;
            }
        }
    }
}
</style>
