<template>
    <div class="chart-conatainer">
        <div class="head">
            <div class="title">Чарт</div>
            <div class="subtitle">Треки, популярные на сайте прямо сейчас</div>
        </div>
        <div class="tracks-container"></div>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
</script>
<style lang="scss" scoped>
.chart-conatainer {
    display: flex;
    flex-direction: column;

    .head {
        display: flex;
        flex-direction: column;

        .title {
            font-size: 24px;
            font-weight: 600;
            color: $primary-text;
        }
        .subtitle {
            font-size: 14px;
            font-weight: 400;
            color: $secondary-text;
        }
    }
}
</style>
