<template>

    <div class="formkit-outer" data-family="box" data-type="checkbox" data-complete="true">
        <label class="formkit-wrapper">
            <div class="formkit-inner">
                <input @change="changed" v-model="modelValue" class="formkit-input" type="checkbox" :name="name"
                    id="input_0" aria-describedby="help-input_0">
                <span class="formkit-decorator" aria-hidden="true">
                    <span class="formkit-decorator-icon formkit-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 27">
                            <polygon fill="currentColor"
                                points="26.99 0 10.13 17.17 4.69 11.63 0 16.41 10.4 27 15.05 22.27 15.09 22.31 32 5.1 26.99 0">
                            </polygon>
                        </svg>
                    </span>
                </span>
            </div>
            <span class="formkit-label" v-if="label">{{ label }}</span>
        </label>
        <div class="formkit-help" id="help-input_0" v-if="help">{{ help }}</div>
    </div>

</template>
<style lang="scss">
.formkit-outer {
    .formkit-wrapper {
        .formkit-inner {
            .formkit-input:checked~.formkit-decorator {
                --cheked-color:var(--yellow);
                box-shadow: 0 0 0 1px var(--cheked-color);

                svg {
                    color: var(--cheked-color);
                }
            }
        }
    }
}
</style>
<script>
export default {
    props: {
        modelValue: Boolean,
        label: String,
        help: String,
        name: String,
    },
    emits: ['update:modelValue'],
    methods: {
        changed(event) {
            this.$emit('update:modelValue', event.target.checked)
        }
    }
}
</script>