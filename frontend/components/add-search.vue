<template>
    <div class="search-container">
        <AppInput
            class="search"
            :placeholder="placeholder"
            v-model="search"
            clearable
        />
        <AppButtonAdd v-if="to" :to="to" />
    </div>
</template>
<script setup>
const props = defineProps({
    search: {
        type: String,
        default: "",
    },
    to: {
        type: Object,
        default: null,
    },
    placeholder: {
        type: String,
        default: null,
    },
});
const emit = defineEmits(["update:search"]);
const search = computed({
    get: () => props.search,
    set: (value) => emit("update:search", value),
});
</script>
<style lang="scss" scoped>
.search-container {
    display: flex;
    gap: 5px;
    .search {
        --app-input-border-radius: 5px;
    }
}
</style>
