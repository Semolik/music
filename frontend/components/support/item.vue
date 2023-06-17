<template>
    <nuxt-link class="item">
        <div class="line">
            <div class="login">
                {{ item.user.username }}
            </div>
            <div class="date">
                {{ date }}
            </div>
        </div>
        <div class="message">
            {{ item.message }}
        </div>
    </nuxt-link>
</template>
<script setup>
import moment from "moment";
const { item } = defineProps({
    item: Object,
});
const date = moment(item.created_at).format("DD.MM.YYYY HH:mm");
</script>
<style lang="scss" scoped>
.item {
    display: flex;
    flex-direction: column;
    padding: 10px;
    border-radius: 10px;
    background-color: $quaternary-bg;
    gap: 10px;
    cursor: pointer;

    .line {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        gap: 10px;
    }

    &:hover {
        background-color: $quinary-bg;
    }
    .login {
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .message {
        overflow-wrap: anywhere;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 1;
        overflow: hidden;
    }
}
</style>
