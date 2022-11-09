<template>
    <div :class="['formkit-outer', { 'off-margin': offMargin }]" data-family="text" data-type="text">
        <div class="formkit-wrapper">
            <label class="formkit-label" :for="id" v-if="label">{{ label }}</label>
            <div class="formkit-inner-container">
                <div :class="['formkit-inner', { error: notValid }, { setColor: !offChangeColor }, formkitInnerClass]"
                    :style="{ '--inner-radius': borderRadius + 'px' }">
                    <slot name="right"></slot>
                    <input v-on="inputEvents || {}" :placeholder="placeholder" class="formkit-input" type="text"
                        :name="name" :id="id" v-model="modelValue">
                    <slot></slot>
                </div>
                <slot name="side"></slot>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
@use '@/assets/styles/helpers';

.formkit-outer {
    &.off-margin {
        margin: 0;
    }

    .formkit-wrapper {
        flex-grow: 1;
        max-width: none;

        .formkit-inner-container {
            display: flex;
            gap: 10px;

            .formkit-inner {
                --accent-color: var(--fields-border-color);
                flex-grow: 1;
                border-radius: var(--inner-radius);
                box-shadow: 0 0 0 1px var(--accent-color);
                overflow: hidden;

                .icon {
                    @include helpers.flex-center;
                    height: 100%;
                    aspect-ratio: 1;
                    background-color: var(--accent-color);
                }

                .count {
                    opacity: 0;
                    padding: 0px 8px;

                    &.wrong {
                        opacity: 1;
                        color: red;
                    }
                }

                &:focus-within {
                    .count {
                        opacity: 1;
                    }

                    &.setColor {
                        --accent-color: var(--purple-1);
                    }

                    box-shadow: 0 0 0 1px var(--accent-color);

                }

                &.error {
                    box-shadow: 0 0 0 1px red;
                }
            }

            .formkit-input {
                color: var(--color-text);
            }
        }
    }
}
</style>
<script>
export default {
    props: {
        label: String,
        id: String,
        name: String,
        placeholder: String,
        modelValue: String,
        borderRadius: Number,
        offMargin: Boolean,
        notEmpty: Boolean,
        offChangeColor: Boolean,
        value: String,
        inputEvents: Object,
        formkitInnerClass: Object
    },
    inject: ['runValidation'],
    data() {
        return {
            notValid: false,
        }
    },
    emits: ['update:modelValue', 'empty'],
    watch: {
        modelValue(value) {
            this.changeValue(value);
        },
        runValidation(value) {
            if (value) {
                this.verify(this.modelValue);
            }
        }
    },
    methods: {
        changeValue(text) {
            // let text = value.target.value;
            this.$emit('update:modelValue', text);
            this.verify(text);

        },
        verify(text) {
            if (this.notEmpty) {
                this.notValid = !Boolean(text)
                this.$emit('empty', !this.notValid);
            }
        }
    }
}
</script>