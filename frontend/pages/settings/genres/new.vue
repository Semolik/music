<template>
    <div class="create-genre-container"></div>
</template>
<script setup>
definePageMeta({
    middleware: ["admin"],
});
</script>
<style scoped lang="scss">
.create-genre-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    .create-genre-form {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        max-width: 500px;
        .create-genre-form__input {
            width: 100%;
            margin-bottom: 20px;
        }
        .create-genre-form__button {
            width: 100%;
            margin-bottom: 20px;
        }
    }
}
</style>
