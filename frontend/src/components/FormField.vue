<template>
    <div class="formkit-outer" data-family="text" data-type="text">
        <div class="formkit-wrapper">
            <label class="formkit-label" :for="id" v-if="label">{{label}}</label>
            <div class="formkit-inner" :style="{'--inner-radius': borderRadius+'px'}">
                <input @input="changeValue" :placeholder="placeholder" class="formkit-input" type="text" :name="name"
                    :id="id" v-model="modelValue">
                <slot></slot>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
.formkit-wrapper {
    max-width: none;

    .formkit-inner {
        border-radius: var(--inner-radius);
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

            border-color: var(--purple-1);
            box-shadow: 0 0 0 1px var(--purple-1);
        }
    }

    .formkit-input {
        color: var(--color-text);
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
    },
    emits: ['update:modelValue'],
    methods: {
        changeValue(value) {
            this.$emit('update:modelValue', value.target.value)
        }
    }
}
</script>