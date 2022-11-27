<template>
    <div class="head">
        <div class="headline">{{ text }}</div>
        <router-link class="back" :to="backUrl" v-if="backUrl">Назад</router-link>
    </div>
</template>
<script>
export default {
    props: {
        text: String,
        backUrl: String
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';

.head {

    @include helpers.flex-center;
    justify-content: space-between;

    .back {
        color: var(--color-text);
        text-decoration: none;
        background-color: var(--color-background-mute-2);
        padding: 5px 20px;
        border-radius: 10px;
        cursor: pointer;

        &:hover {
            background-color: var(--color-background-mute-3);
        }
    }
}
</style>