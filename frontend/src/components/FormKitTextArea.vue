<template>
    <div class="formkit-wrapper">
        <label class="formkit-label" :for="`input_${name}`" v-if="label">{{label}}</label>
        <div class="formkit-inner">
            <textarea rows="10" :placeholder="placeholder" class="formkit-input" :name="name" :id="`input_${name}`"
                aria-describedby="help-input_0"></textarea>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        label: String,
        placeholder: String,
        name: String,
    }
}
</script>
<style lang="scss">
.formkit-wrapper {
    max-width: 100%;
    width: 100%;

    textarea {
        resize: none;
    }
}
</style>