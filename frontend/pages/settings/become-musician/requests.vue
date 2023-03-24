<template>
    <div class="requests-page">
        <div class="requests-container">
            <RequestsInfoFull
                :request="request"
                v-for="request in requests"
                :key="request.id"
            />
        </div>
        <AppButton @click="loadMore" active v-if="showButton">
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
definePageMeta({
    middleware: ["auth"],
});
const runtimeConfig = useRuntimeConfig();
const { CHANGE_ROLE_PAGE_ITEMS } = runtimeConfig.public;
const page = ref(1);
const requests = ref(
    await Service.getChangeRequestsApiV1RolesChangeGet(page.value)
);
const showButton = ref(requests.value.length === CHANGE_ROLE_PAGE_ITEMS);
const loadMore = async () => {
    page.value++;
    const newRequests = await Service.getChangeRequestsApiV1RolesChangeGet(
        page.value
    );
    showButton.value = newRequests.length === CHANGE_ROLE_PAGE_ITEMS;
    requests.value = [...requests.value, ...newRequests];
};
</script>
<style scoped lang="scss">
.requests-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .requests-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
