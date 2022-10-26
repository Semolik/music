<template>
    <textarea :name="name" v-model="modelValue" id="" :placeholder="placeholder" :cols="cols" :rows="rows"
        :style="{ '--radius': borderRadius+'px' }"></textarea>
</template>
<script>
export default {
    props: {
        modelValue: String,
        name: String,
        rows: Number,
        cols: Number,
        borderRadius: Number,
        placeholder: String,
    },
    emits: ['update:modelValue'],
    methods: {
        updateValue(event) {
            let text = event.target.value;
            this.$emit('update:modelValue', text);
        }
    }
}
</script>
<style lang="scss">
textarea {
    width: 100%;
    resize: none;
    border: none;
    box-shadow: 0 0 0 1px var(--fields-border-color);
    outline: none;
    background-color: transparent;
    border-radius: var(--radius);
    padding: 10px;
    color: var(--color-text);
    font-size: 1.1em;

    &:focus {
        box-shadow: 0 0 0 1px var(--purple-1);
    }
}
</style>