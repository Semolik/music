<template>
    <nuxt-link
        class="item"
        :to="{
            name: routesNames.adminCabinet.cabinetSupportId,
            params: { id: item.id },
        }"
    >
        <div class="line">
            <div class="login">
                {{ item.login }}
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
import { routesNames } from "@typed-router";
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

        .message {
            background-color: $senary-bg;
        }
    }
    .login {
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .message {
        overflow-wrap: anywhere;
        @include clip-text(2);
        background-color: $quinary-bg;
        padding: 10px;
        flex-grow: 1;
        border-radius: 5px;
    }
}
</style>
