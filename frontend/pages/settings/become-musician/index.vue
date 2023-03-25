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
            <div :class="['files', { 'has-files': files.length > 0 }]">
                <div class="files-list">
                    <div class="add-file-button">
                        <Icon name="material-symbols:attach-file" />
                        <input
                            type="file"
                            multiple
                            :title="filesNames"
                            @change="handleFileChange"
                        />
                    </div>
                    <div
                        v-for="file in files"
                        :key="file.name"
                        class="file"
                        @click="deleteFile(file)"
                    >
                        {{ file.name }}
                    </div>
                </div>
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
                class="show-requests-button"
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
const runtimeConfig = useRuntimeConfig();
const { MAX_CHANGE_ROLE_FILES_SIZE_MB } = runtimeConfig.public;
const message = ref("");
const currentRequest = ref(
    await Service.getCurrentChangeRequestApiV1RolesChangeCurrentGet()
);
const hasRequests = currentRequest.value
    ? false
    : await Service.hasChangeRequestsApiV1RolesChangeHasGet();
const files = ref([]);
const filesNames = computed(() => {
    if (files.value.length === 0) return "Выберите файлы";
    return files.value.map((file) => file.name).join(", ");
});
const deleteFile = (file) => {
    files.value = files.value.filter((f) => f !== file);
};
const handleFileChange = (e) => {
    const fileArray = Array.from(e.target.files);
    const filesSize = fileArray
        .map((file) => file.size)
        .reduce((acc, size) => acc + size, 0);
    if (filesSize > MAX_CHANGE_ROLE_FILES_SIZE_MB * 1024 * 1024) {
        toast.error(
            `Максимальный размер файлов ${MAX_CHANGE_ROLE_FILES_SIZE_MB} МБ`
        );
        return;
    }
    files.value = fileArray;
};
const send = async () => {
    if (message.value.length === 0) {
        toast.error("Сообщение не может быть пустым");
        return;
    }
    try {
        currentRequest.value =
            await Service.sendUpdateRoleRequestApiV1RolesChangePost({
                message: message.value,
                files: files.value,
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
.files {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .files-list {
        display: flex;
        gap: 10px;
        .file {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-radius: 5px;
            background-color: $secondary-bg;
            transition: all 0.2s ease-in-out;
            &:hover {
                background-color: $accent;
                cursor: pointer;
            }
        }
    }

    &.has-files {
        flex-direction: row;
        .add-file-button {
            width: 40px;
        }
    }
    .add-file-button {
        @include flex-center;
        width: 100%;
        height: 40px;
        border: 2px dashed $secondary-text;
        border-radius: 5px;
        transition: all 0.2s ease-in-out;
        position: relative;
        isolation: isolate;

        &:hover {
            border-color: $accent;
            cursor: pointer;
        }

        svg {
            width: 20px;
            height: 20px;
            fill: $secondary-text;
        }
        input {
            z-index: 1;
            opacity: 0;
            position: absolute;
            inset: 0;
            cursor: pointer;
        }
    }
}
</style>
