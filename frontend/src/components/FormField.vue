<template>
    <div class="formkit-outer" data-family="text" data-type="text">
        <div class="formkit-wrapper">
            <label class="formkit-label" :for="id" v-if="label">{{label}}</label>
            <div class="formkit-inner">
                <input @input="changeValue" :placeholder="placeholder" class="formkit-input" type="text" :name="name"
                    :id="id" v-model="modelValue">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        label: String,
        id: String,
        name: String,
        placeholder: String,
        modelValue: String,
    },
    emits: ['update:modelValue'],
    methods: {
        changeValue(value) {
            this.$emit('update:modelValue', value.target.value)
        }
    }
}
</script>