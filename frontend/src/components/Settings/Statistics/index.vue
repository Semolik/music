<template>
    <div class="statistics-container">
        <div class="statistics-items">
            <div class="statistics-item">
                <div class="item__value">{{ user_count }}</div>
                <div class="item__title">Пользователей</div>
            </div>
            <div class="statistics-item">
                <div class="item__value">{{ musician_count }}</div>
                <div class="item__title">Музыкантов</div>
            </div>
            <div class="statistics-item">
                <div class="item__value">{{ admin_count }}</div>
                <div class="item__title">Администраторов</div>
            </div>
            <router-link
                :to="{ path: '/lk/update-status-requests' }"
                class="statistics-item"
            >
                <div class="item__value">{{ change_role_request_count }}</div>
                <div class="item__title">
                    Активных заявок на смену типа аккаунта
                </div>
            </router-link>
        </div>
    </div>
</template>
<script setup>
import { HTTP } from "/src/http-common.vue";
const { data } = await HTTP.get("/statistics");
const { user_count, admin_count, musician_count, change_role_request_count } =
    data;
</script>
<style lang="scss">
@use "@/assets/styles/helpers";
@use "@/assets/styles/breakpoints";

.statistics-container {
    display: flex;
    flex-direction: column;

    .statistics-items {
        display: grid;
        grid-template-rows: min-content;
        gap: 10px;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        a:hover.statistics-item {
            background-color: var(--color-background-mute-4);
        }
        .statistics-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            background-color: var(--color-background-mute-3);
            border-radius: 15px;
            padding: 20px;
            flex-grow: 1;
            gap: 10px;
            text-decoration: none;
            color: var(--color-text);
            .item__value {
                font-size: 2.5rem;
                font-weight: 600;
            }
        }
    }
}
</style>
