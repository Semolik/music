<template>
    <div :class="['formkit-outer', {'off-margin': offMargin}]" data-family="text" data-type="text">
        <div class="formkit-wrapper">
            <label class="formkit-label" :for="id" v-if="label">{{label}}</label>
            <div class="formkit-inner-container">
                <div class="formkit-inner" :style="{'--inner-radius': borderRadius+'px'}">
                    <input @input="changeValue" :placeholder="placeholder" class="formkit-input" type="text"
                        :name="name" :id="id" v-model="modelValue">
                    <slot></slot>
                </div>
                <slot name="side"></slot>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
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
                flex-grow: 1;
                border-radius: var(--inner-radius);
                box-shadow: 0 0 0 1px var(--fields-border-color);

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

                    box-shadow: 0 0 0 1px var(--purple-1);
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
    },
    emits: ['update:modelValue'],
    methods: {
        changeValue(value) {
            this.$emit('update:modelValue', value.target.value)
        }
    }
}
</script>