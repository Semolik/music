<template>
    <header>
        <div class="search-button" @click="searchIsActive = true">
            <Icon name="material-symbols:search-rounded" />
            <span class="button-text"> Поиск </span>
            <span class="button-hotkey-text"> Ctrl + K </span>
        </div>
        <AppHeaderSearch v-model:searchActive="searchIsActive" />
    </header>
</template>
<script setup>
const searchIsActive = ref(false);

onMounted(() => {
    window.addEventListener("keydown", (event) => {
        if (event.ctrlKey && event.key === "k") {
            event.preventDefault();
            searchIsActive.value = !searchIsActive.value;
        }
        if (event.key === "Escape") {
            searchIsActive.value = false;
        }
    });
});

onUnmounted(() => {
    window.removeEventListener("keydown", () => {});
});
</script>
<style lang="scss">
header {
    padding: 20px;
    display: flex;

    .search-button {
        @include flex-center;
        flex-grow: 1;
        gap: 10px;
        padding: 10px;
        border-radius: 10px;
        color: $secondary-text;
        height: min-content;
        cursor: pointer;
        background-color: $tertiary-bg;
        &:hover {
            background-color: $quaternary-bg;
        }

        svg {
            width: 20px;
            height: 20px;
        }
        .button-text {
            flex-grow: 1;
        }
        .button-hotkey-text {
            border-radius: 5px;
            color: $secondary-text;
            border: 1px solid $secondary-text;
            padding: 3px 5px;
            user-select: none;
        }
    }
}
</style>
