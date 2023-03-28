<template>
    <div class="profile">
        <div class="profile-editor">
            <div class="avatar-contaner">
                <Upload
                    action="/api/v1/users/me/public/avatar"
                    method="PUT"
                    :on-success="handleAvatarSuccess"
                    :imageUrl="publicProfileData.picture"
                    border-radius="50%"
                    class="avatar-uploader"
                    name="userPublicPicture"
                />
                <div
                    :class="[
                        'delete-button-contaner',
                        { active: publicProfileData.picture },
                    ]"
                >
                    <div
                        class="delete-button"
                        @[publicProfileData.picture&&`click`]="
                            showDeleteAvatarModal = true
                        "
                    >
                        <Icon :name="IconsNames.deleteIcon" />
                    </div>
                </div>
                <ModalDialog
                    :active="showDeleteAvatarModal"
                    @close="showDeleteAvatarModal = false"
                    :buttons="[
                        {
                            text: 'Удалить',
                            type: 'danger',
                            onClick: deleteUserAvatar,
                        },
                        {
                            text: 'Отмена',
                            type: 'primary',
                            onClick: () => {
                                showDeleteAvatarModal = false;
                            },
                        },
                    ]"
                >
                    <template #content>
                        <div class="warning-modal">
                            <div class="warning-modal-headline">
                                Вы уверены, что хотите удалить аватар?
                            </div>
                        </div>
                    </template>
                </ModalDialog>
            </div>
            <div class="profile-form-fields">
                <AppInput
                    v-model="name"
                    label="Имя"
                    :max-length="MAX_PUBLIC_PROFILE_NAME_LENGTH"
                    :min-length="1"
                    show-word-limit
                    :error="nameError"
                />
                <AppInput
                    v-model="description"
                    label="Описание"
                    :max-length="MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH"
                    show-word-limit
                    :error="descriptionError"
                    type="textarea"
                    :rows="3"
                    resize="none"
                    @max-length="
                        (e) =>
                            toast.error(
                                `Максимальная длина описания - ${MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH} символов`
                            )
                    "
                />

                <AppInput
                    v-model="links.vk"
                    label="Ссылка на ВК"
                    :error="!vkIsCorrect"
                    prepend="https://vk.com/"
                />
                <AppInput
                    v-model="links.telegram"
                    label="Ссылка на Telegram"
                    :error="!telegramIsCorrect"
                    prepend="https://t.me/"
                />
                <AppInput
                    v-model="links.youtube"
                    label="Ссылка на YouTube"
                    :error="!youtubeIsCorrect"
                    prepend="https://www.youtube.com/channel/"
                />
            </div>

            <AppButton @click="saveProfile" :active="buttonActive">
                Сохранить
            </AppButton>
        </div>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
import { IconsNames } from "~~/configs/icons";

import { useToast } from "vue-toastification";
useHead({ title: "Профиль" });
definePageMeta({
    middleware: ["auth"],
});
const toast = useToast();

const {
    MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH,
    MAX_PUBLIC_PROFILE_NAME_LENGTH,
    MAX_TELEGRAM_USERNAME_LENGTH,
    MAX_YOUTUBE_CHANNEL_ID_LENGTH,
    MAX_VK_USERNAME_LENGTH,
} = useRuntimeConfig().public;
const publicProfileData = reactive(
    await Service.getUserPublicProfileInfoApiV1UsersMePublicGet()
);
const name = ref(publicProfileData.name);
const description = ref(publicProfileData.description || "");
const links = reactive(Object.assign({}, publicProfileData.links));

const vkIsCorrect = computed(() => {
    if (!links.vk) {
        return true;
    }
    return links.vk.length <= MAX_VK_USERNAME_LENGTH;
});

const telegramIsCorrect = computed(() => {
    if (!links.telegram) {
        return true;
    }
    return links.telegram.length <= MAX_TELEGRAM_USERNAME_LENGTH;
});
const youtubeIsCorrect = computed(() => {
    if (!links.youtube) {
        return true;
    }
    return links.youtube.length <= MAX_YOUTUBE_CHANNEL_ID_LENGTH;
});

const showDeleteAvatarModal = ref(false);

const nameError = computed(
    () =>
        name.value.length === 0 ||
        name.value.length > MAX_PUBLIC_PROFILE_NAME_LENGTH
);
const descriptionError = computed(
    () => description.value.length > MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH
);

const buttonActive = computed(() => {
    return (
        !nameError.value &&
        !descriptionError.value &&
        vkIsCorrect.value &&
        telegramIsCorrect.value &&
        youtubeIsCorrect.value &&
        (name.value !== publicProfileData.name ||
            description.value !== publicProfileData.description ||
            publicProfileData.links.vk !== links.vk ||
            publicProfileData.links.telegram !== links.telegram ||
            publicProfileData.links.youtube !== links.youtube)
    );
});
const saveProfile = async () => {
    if (buttonActive.value) {
        try {
            const response =
                await Service.updateUserPublicProfileDataApiV1UsersMePublicPut({
                    name: name.value,
                    description: description.value,
                    vk: links.vk,
                    telegram: links.telegram,
                    youtube: links.youtube,
                });
            publicProfileData.name = name.value;
            publicProfileData.description = description.value;
            for (const key in response) {
                publicProfileData[key] = response[key];
            }
            for (const key in links) {
                links[key] = links[key];
            }
        } catch (error) {
            toast.error(HandleOpenApiError(error).message);
        }
    }
};
const handleAvatarSuccess = (response, uploadFile) => {
    publicProfileData.picture = response.picture;
};
const deleteUserAvatar = async () => {
    try {
        await Service.updateUserPublicAvatarApiV1UsersMePublicAvatarPut();
        publicProfileData.picture = null;
    } catch (error) {
        toast.error(HandleOpenApiError(error).message);
    }
    showDeleteAvatarModal.value = false;
};
</script>

<style lang="scss" scoped>
.profile {
    @include flex-center;
    @include sm {
        padding: 1rem;
    }
    .profile-editor {
        max-width: 500px;
        width: 100%;
        display: flex;
        gap: 10px;
        flex-direction: column;
        @include flex-center;

        .avatar-contaner {
            @include flex-center;
            gap: 10px;
            position: relative;
            max-width: 150px;
            aspect-ratio: 1;
            width: 100%;

            .avatar-uploader {
                width: 100%;
                height: 100%;
            }
            .delete-button-contaner {
                position: absolute;
                top: 0;
                bottom: 0;
                left: calc(103%);
                @include flex-center;
                opacity: 0;

                &.active {
                    opacity: 1;
                }
                .delete-button {
                    @include flex-center;
                    border-radius: 50%;
                    cursor: pointer;
                    background-color: $quinary-bg;
                    padding: 10px;
                    height: min-content;
                    @include lg {
                        &:hover {
                            background-color: $accent-red;
                        }
                    }
                }
            }
        }
        .profile-form-fields {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 100%;
            .line {
                display: flex;
                gap: 10px;
                width: 100%;
            }
        }
    }
}
</style>
