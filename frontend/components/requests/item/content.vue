<template>
    <UserAvatar :picture="request.user.picture" />
    <div class="info">
        <div class="user-name">{{ fullName }}</div>
        <div class="date">
            {{ time_created }}
        </div>
    </div>
    <div :class="['status', request.request_status]" v-if="showStatus">
        <Icon :name="icones[request.request_status]" />
    </div>
</template>
<script setup>
import { ChangeRoleRequestStatus } from "@/client";
import moment from "moment";
const { request, showStatus } = defineProps({
    request: Object,
    showStatus: Boolean,
});
const icones = {
    [ChangeRoleRequestStatus.REJECTED]: "material-symbols:close-rounded",
    [ChangeRoleRequestStatus.ACCEPTED]: "ic:check",
    [ChangeRoleRequestStatus.IN_PROGRESS]:
        "material-symbols:hourglass-bottom-rounded",
};
const time_created = computed(() =>
    moment(request.time_created).format("DD.MM.YYYY HH:mm")
);

const fullName = computed(() => useFullName(request.user));
</script>
<style lang="scss" scoped>
.info {
    display: flex;
    flex-direction: column;
    color: $secondary-text;

    .user-name {
        font-size: 16px;
        font-weight: 500;
        color: $primary-text;
    }
}
.status {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 5px;
    svg {
        width: 20px;
        height: 20px;
    }

    &.rejected {
        color: $accent-error;
    }
    &.in-progress {
        color: $accent-warning;
    }
    &.accepted {
        color: $accent-success;
    }
}
</style>
