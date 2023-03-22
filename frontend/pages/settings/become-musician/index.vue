<template>
    <SettingsPage
        title="Стать музыкантом"
        padding="10px"
        max-width="100%"
        :title-button-text="hasRequests && 'История запросов'"
        :title-button-to-name="routesNames.settings.becomeMusician"
    >
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
            />
        </div>
        <AppButton
            class="become-musician-button"
            @click="send"
            :active="message.length > 0"
        >
            Отправить
        </AppButton>
    </SettingsPage>
</template>
<script setup>
import { routesNames } from "~~/.nuxt/typed-router";
import { Service } from "~~/client";
import { useToast } from "vue-toastification";
definePageMeta({
    middleware: ["auth"],
});
const toast = useToast();
const message = ref("");
const hasRequests = ref(
    await Service.userHasChangeRequestsApiV1RolesChangeHasGet()
);

const send = async () => {
    try {
        await Service.sendUpdateRoleRequestApiV1RolesChangePost({
            message: message.value,
        });
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
</script>
<style lang="scss">
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
