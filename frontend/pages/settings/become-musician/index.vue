<template>
    <SettingsPage title="Стать музыкантом" padding="10px" max-width="100%">
        <div class="message" v-if="isAdmin">
            Администратор не может отправить запрос на изменение роли.
        </div>
        <template v-else-if="!currentRequest">
            <div id="become-musician">
                <div class="become-musician-head-text">
                    Подвердите, что вы являетесь музыкантом, сообщение будет
                    отправлено администратору сайта.
                </div>
                <AppInput
                    type="textarea"
                    placeholder="Напишите сообщение"
                    v-model="message"
                    rows="8"
                    name="message"
                    resize="none"
                />
            </div>
            <AppButton
                class="become-musician-button"
                @click="send"
                :active="message.length > 0"
            >
                Отправить
            </AppButton>
            <AppButton
                v-if="hasRequests"
                class="become-musician-button"
                @click="
                    () =>
                        $router.push({
                            name: routesNames.settings.becomeMusicianRequests,
                        })
                "
            >
                Посмотреть запросы
            </AppButton>
        </template>
        <template v-else>
            <RequestsInfoFull :request="currentRequest" />
            <AppButton active class="delete-button" @click="deleteRequest">
                Удалить
            </AppButton>
        </template>
    </SettingsPage>
</template>
<script setup>
import { Service } from "~~/client";
import { useToast } from "vue-toastification";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "@typed-router";
definePageMeta({
    middleware: ["auth"],
});
const authStore = useAuthStore();
const { isAdmin } = storeToRefs(authStore);
const toast = useToast();
const message = ref("");
const currentRequest = ref(
    await Service.getCurrentChangeRequestApiV1RolesChangeCurrentGet()
);
const router = useRouter();
const hasRequests = currentRequest.value
    ? false
    : await Service.hasChangeRequestsApiV1RolesChangeHasGet();
const send = async () => {
    try {
        currentRequest.value =
            await Service.sendUpdateRoleRequestApiV1RolesChangePost({
                message: message.value,
            });
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
const deleteRequest = async () => {
    try {
        await Service.deleteChangeRoleRequestApiV1RolesChangeRequestIdDelete(
            currentRequest.value.id
        );
        currentRequest.value = null;
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
</script>
<style lang="scss" scoped>
.message {
    color: $secondary-text;
    text-align: center;
    height: 100%;
    flex-grow: 1;
    @include flex-center;
}
.delete-button {
    --app-button-active-bg: #{$accent-red};
    --app-button-active-hover-bg: #{$accent-error};
}
#become-musician {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .become-musician-head-text {
        color: $secondary-text;
    }
    textarea {
        resize: none;
    }
}
</style>
