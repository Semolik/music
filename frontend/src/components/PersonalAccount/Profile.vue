<template>
    <div class="profile-container">
        <form class="user-info-container" @submit.prevent="formSubmited" ref="form" id="user-info-container">
            <SelectImage @changed="updatePic" :pictureUrl="picture" name="userPicture" ref="selectPic" />
            <div class="button remove-picture" v-if="!avatarIsEmpty" @click="detelePicture">
                <FontAwesomeIcon icon="fa-trash" />
            </div>
            <div class="user-info">
                <div class="fields">
                    <FormField :borderRadius="10" name="first_name" label="Имя" placeholder="Ваше имя"
                        v-model="firstName">
                        <span :class="['count', { wrong: firstNameLenght < 0 }]">{{ firstNameLenght }}</span>
                    </FormField>
                    <FormField :borderRadius="10" name="last_name" label="Фамилия" placeholder="Ваша фамилия"
                        v-model="lastName">
                        <span :class="['count', { wrong: lastNameLenght < 0 }]">{{ lastNameLenght }}</span>
                    </FormField>
                </div>
                <div class="user-information" v-if="userData">
                    <div class="block">username: {{ userData.username }}</div>
                    <div class="block custom">тип аккаунта:
                        <div class="statuses">
                            <span :class="{ active: userRole === Role.Musician }">музыкант</span>
                            <span :class="{ active: userRole === Role.User }">пользователь</span>
                            <span :class="{ active: userRole === Role.RadioStation }">радиостанция</span>
                        </div>
                    </div>
                </div>
                <Teleport :disabled="avatarIsEmpty" to="#user-info-container" v-if="mounted">
                    <SaveBlock @click="save" :active="dataChanged" :wrong="fieldsWrong" />
                </Teleport>
            </div>
        </form>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser, faFloppyDisk, faTrash, faImage } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { storeToRefs } from 'pinia';
import { HTTP } from '/src/http-common.vue';
import { useAuthStore } from '/src/stores/auth';
import handleError from '/src/composables/errors';
import { useToast } from "vue-toastification";
import FormField from '/src/components/FormField.vue';
import AnimateInteger from '/src/components/AnimateInteger.vue';
import { Role } from '/src/helpers/roles.js';
import SelectImage from '/src/components/SelectImage.vue';
import SaveBlock from '/src/components/PersonalAccount/SaveBlock.vue';

library.add([faUser, faFloppyDisk, faTrash, faImage])

export default {
    setup() {
        const { userData, userRole } = storeToRefs(useAuthStore());
        const { setUserData, logout, getMe } = useAuthStore();
        const toast = useToast();
        const { VITE_MAX_FIRSTNAME_LENGTH, VITE_MAX_LASTNAME_LENGTH } = import.meta.env;
        return {
            userData,
            toast,
            setUserData,
            logout,
            getMe,
            Role,
            userRole,
            VITE_MAX_FIRSTNAME_LENGTH,
            VITE_MAX_LASTNAME_LENGTH,
        }
    },
    data() {
        return {
            firstName: this.userData?.first_name,
            lastName: this.userData?.last_name,
            mounted: false,
            remove_picture: false,
            original_image: null,
            file_changed: false,
            fileChanged: false,
            picture: this.userData?.picture,
        }
    },
    mounted() {
        this.mounted = true;
        this.getMe();
    },
    components: {
        FontAwesomeIcon,
        FormField,
        AnimateInteger,
        SelectImage,
        SaveBlock
    },
    watch: {
        userData(value) {
            if (!value) return
            const { first_name, last_name, picture } = value;
            this.firstName = first_name;
            this.lastName = last_name;
            this.original_image = picture;
        }
    },
    methods: {
        detelePicture() {
            this.$refs.selectPic.detelePicture();
            this.remove_picture = true;
            this.file_changed = true;
        },
        updatePic(target) {
            this.file_changed = true;
            if (!this.file_changed) return
            let file = target.files;
            this.fileChanged = file !== this.userData.picture;
        },
        save() {
            if (this.dataChanged) {
                const form = this.$refs.form;
                if (!form) return
                let data = new FormData(form);
                data.append('remove_picture', this.remove_picture);
                HTTP.put('me', data)
                    .then((response) => {
                        this.remove_picture = false;
                        this.file_changed = false;
                        this.setUserData(response.data);
                    })
                    .catch((error) => {
                        this.toast.error(handleError(error, 'При обновлении профиля произошла ошибка').message)
                    });
            }
        }
    },
    computed: {
        avatarIsEmpty() {
            if (!this.userData) return true
            return !Boolean(this.userData.picture)
        },
        dataChanged() {
            if (!this.userData) return
            if (this.fieldsWrong) return
            return this.userData.first_name !== this.firstName || this.userData.last_name !== this.lastName || this.file_changed
        },
        fieldsWrong() {
            return this.lastNameLenght < 0 || this.firstNameLenght < 0
        },
        lastNameLenght() {
            if (!this.lastName) return
            return this.VITE_MAX_LASTNAME_LENGTH - this.lastName?.length
        },
        firstNameLenght() {
            if (!this.firstName) return
            return this.VITE_MAX_FIRSTNAME_LENGTH - this.firstName?.length
        },
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.profile-container {
    display: flex;
    flex-direction: column;

    .user-info-container {
        display: grid;
        gap: 10px;
        grid-template-columns: 200px 1fr;

        @include breakpoints.lg(true) {
            grid-template-columns: 160px 1fr;
        }

        @include breakpoints.sm(true) {
            grid-template-columns: 1fr;
        }

        .user-pic {
            aspect-ratio: 1;
            position: relative;
            overflow: hidden;
            border-radius: 7px;
            transition: 2s filter, 2s opacity;

            img {
                object-fit: cover;
                width: 100%;
                height: 100%;
            }

            &.empty {
                @include helpers.flex-center;
                overflow: hidden;
                border: 2px dashed transparent;
                border-color: var(--main-card-border);


                svg {
                    width: 50px;
                    height: 50px;

                }

                .edit-area {
                    .edit-area-text {
                        margin-top: 90px;
                    }
                }
            }

            &:hover {
                .edit-area {
                    opacity: 1;
                }

                img {
                    filter: blur(3px);
                }
            }

            .edit-area {
                transition: opacity .2s;
                @include helpers.flex-center;
                flex-direction: column;
                position: absolute;
                inset: 0;
                opacity: 0;
                isolation: isolate;

                .edit-area-container {
                    z-index: 2;
                    position: absolute;
                    inset: 0;
                    @include helpers.flex-center;
                    flex-direction: column;
                    background-color: rgba($color: #000000, $alpha: 0.2);
                    padding: 5px;
                    // border-radius: 10px;
                    aspect-ratio: 1;

                    svg {
                        width: 30px;
                        height: 30px;
                        margin-bottom: 10px;
                        z-index: 2;
                    }

                    .edit-area-text {

                        z-index: 2;
                    }

                }

                input {
                    position: absolute;
                    inset: 0;
                    z-index: 3;
                    opacity: 0;
                    cursor: pointer;
                }

                &::after {
                    content: '';
                    position: absolute;
                    inset: 0;
                    background-color: var(--color-background-mute-3);
                    opacity: 0.5;
                    z-index: 1;
                }
            }
        }

        .button {
            cursor: pointer;
            padding: 10px;
            background-color: var(--color-background-mute-4);
            border-radius: 10px;
            transition: .2s scale, .2s background-color;

            svg {
                height: 18px;
            }

            &:hover {
                background-color: var(--color-background-mute-5);
            }

            &:active {
                scale: 1.01;
            }
        }

        .remove-picture {
            grid-row: 2;
            @include helpers.flex-center;
        }

        .user-info {
            border-radius: 5px;
            display: grid;
            grid-template-rows: min-content min-content;
            gap: 5px;
            padding-top: 5px;

            .fields {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;

                @include breakpoints.lg(true) {
                    grid-template-columns: 2fr;
                }
            }

            .user-information {
                display: flex;
                gap: 5px;
                flex-wrap: wrap;

                .block {
                    background-color: var(--color-background-mute-4);
                    padding: 5px 15px;
                    border-radius: 15px;
                    @include helpers.flex-center;
                    gap: 10px;
                    flex-grow: 1;

                    &.custom {
                        padding-right: 5px;
                        text-align: center;
                    }

                    .statuses {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 5px;
                        flex-grow: 1;

                        span {
                            background-color: var(--color-background-mute-6);
                            border-radius: 10px;
                            padding: 2px 10px;
                            flex-grow: 1;
                            text-align: center;

                            &.active {
                                background-color: var(--purple);

                            }
                        }
                    }
                }
            }
        }
    }
}
</style>
