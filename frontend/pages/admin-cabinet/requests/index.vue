<template>
    <div class="admin-cabinet-requests-page">
        <div class="filters-panel">
            <div
                :class="['filter', { active: status === null }]"
                @click="onChangeFilter(null)"
            >
                Все
            </div>
            <div
                v-for="(name, key) in statuses"
                :class="['filter', { active: status === key }, key]"
                @click="onChangeFilter(key)"
            >
                {{ name }}
            </div>
        </div>
        <ClientOnly>
            <div class="requests-list" v-auto-animate>
                <RequestsItem
                    v-for="request in requests"
                    :request="request"
                    :key="request.id"
                    :show-status="showStatus"
                />
            </div>
        </ClientOnly>
        <div class="empty" v-if="requestsEmpty">
            По данному запросу ничего не найдено
        </div>
        <AppButton
            class="show-more-button"
            @click="showMore"
            v-if="showMoreButton"
        >
            Показать еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service, ChangeRoleRequestStatus } from "@/client";

definePageMeta({
    middleware: ["admin"],
});
useHead({ title: "Запросы стать музыкантом" });

const statuses = {
    [ChangeRoleRequestStatus.IN_PROGRESS]: "В обработке",
    [ChangeRoleRequestStatus.ACCEPTED]: "Принят",
    [ChangeRoleRequestStatus.REJECTED]: "Отклонен",
};
const status = ref(ChangeRoleRequestStatus.IN_PROGRESS);
const showStatus = computed(() => status.value === null);
const getRequests = async (page, filter) => {
    return await Service.getAllChangeRoleRequestsApiV1RolesChangeAllGet(
        page,
        filter
    );
};
const page = ref(1);

const requests = ref(await getRequests(page.value, status.value));
const requestsEmpty = computed(() => requests.value.length === 0);
const showMoreButton = computed(() => {
    if (page.value === 1) {
        return requests.value.length === 10;
    }
    return true;
});
const showMore = async () => {
    page.value++;
    const newRequests = await getRequests(page.value, status.value);
    requests.value = [...requests.value, ...newRequests];
};
const onChangeFilter = async (filter) => {
    status.value = filter;
    page.value = 1;
    requests.value = await getRequests(page.value, status.value);
};
</script>
<style lang="scss" scoped>
.admin-cabinet-requests-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
    gap: 5px;
    .filters-panel {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        width: 100%;
        .filter {
            background-color: $quinary-bg;
            padding: 5px 20px;
            border-radius: 5px;
            cursor: pointer;
            color: $primary-text;
            user-select: none;
            flex-grow: 1;
            text-align: center;
            &.active {
                background-color: $accent;
                color: $primary-bg;
            }
        }
    }
    .requests-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 5px;
        overflow: hidden;
        width: 100%;
    }
    .empty {
        color: $secondary-text;
        height: 100%;
        @include flex-center;
    }
}
</style>
