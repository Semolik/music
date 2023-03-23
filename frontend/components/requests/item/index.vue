<template>
    <nuxt-link
        class="request"
        :to="{
            name: routesNames.adminCabinet.cabinetRequestsId,
            params: { id: request.id },
        }"
    >
        <RequestsItemContent :request="request" :showStatus="showStatus" />
    </nuxt-link>
</template>
<script setup>
import { routesNames } from "@typed-router";
const { request, showStatus } = defineProps({
    request: Object,
    showStatus: Boolean,
});
</script>
<style lang="scss" scoped>
.request {
    display: flex;
    align-items: center;
    padding: 10px;
    border-radius: 10px;
    background-color: $quaternary-bg;
    gap: 10px;

    &:hover {
        background-color: $quinary-bg;
    }
}
</style>
