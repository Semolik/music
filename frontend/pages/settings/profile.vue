<template>
    <div class="profile">
        <div class="avatar-contaner">
            <Upload
                action="/api/v1/users/me/avatar"
                method="PUT"
                :on-success="handleAvatarSuccess"
                :imageUrl="userInfo.picture"
                border-radius="50%"
                class="avatar-uploader"
                name="userPicture"
            />
            <div
                :class="[
                    'delete-button-contaner',
                    { active: userInfo.picture },
                ]"
            >
                <div
                    class="delete-button"
                    @[userInfo.picture&&`click`]="showDeleteAvatarModal = true"
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
    </div>
</template>
<script setup>
import { Service } from "~~/client";
import { IconsNames } from "~~/configs/icons";
definePageMeta({
    middleware: ["auth"],
});
const showDeleteAvatarModal = ref(false);
const userInfo = ref({});
onMounted(async () => {
    userInfo.value = await Service.getUserInfoApiV1UsersMeGet();
});
const handleAvatarSuccess = (response, uploadFile) => {
    userInfo.value.picture = response.picture;
};
const deleteUserAvatar = async () => {
    userInfo.value = await Service.updateUserAvatarApiV1UsersMeAvatarPut();
    showDeleteAvatarModal.value = false;
};
</script>

<style lang="scss" scoped>
.profile {
    display: flex;
    flex-direction: column;
    @include flex-center;
    gap: 20px;
    .avatar-contaner {
        @include flex-center;
        gap: 10px;
        position: relative;
        max-width: 150px;
        aspect-ratio: 1;
        width: 100%;
        @include lg {
            max-width: 200px;
        }
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
}
</style>
