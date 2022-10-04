<template>
    <div class="profile-container">
        <form class="user-info-container" @submit.prevent="formSubmited" ref="form">
            <div :class="['user-pic', {empty: avatarIsEmpty}]">
                <FontAwesomeIcon icon="fa-user" v-if="avatarIsEmpty" />
                <div class="edit-area">
                    <div class="edit-area-text">выбрать файл</div>
                    <input type="file" name="userPicture">
                </div>
            </div>
            <div class="user-info">
                <div class="fields">
                    <FormKit type="text" name="first_name" label="Имя" v-model="firstName" placeholder="Ваше имя" />
                    <FormKit type="text" name="last_name" label="Фамилия" v-model="lastName"
                        placeholder="Ваша фамилия" />
                </div>
                <div class="buttons">
                    <div :class="['button', 'save', {active: dataChanged}]" @click="save">
                        <FontAwesomeIcon icon="fa-floppy-disk" />
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser, faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { storeToRefs } from 'pinia';
import { HTTP } from '../http-common.vue';
import { useAuthStore } from '../stores/auth';
import handleError from '../composables/errors';
import { useToast } from "vue-toastification";

library.add([faUser, faFloppyDisk])

export default {
    setup() {
        const { userData } = storeToRefs(useAuthStore());
        const toast = useToast();
        return {
            userData,
            toast
        }
    },
    data() {
        return {
            firstName: this.userData?.first_name,
            lastName: this.userData?.last_name,
        }
    },
    components: {
        FontAwesomeIcon,
    },
    watch: {
        userData(value) {
            this.firstName = value?.first_name;
            this.lastName = value?.last_name
        }
    },
    methods: {
        save() {
            if (this.dataChanged) {
                const form = this.$refs.form;
                if (!form) return
                const data = new FormData(form);
                HTTP.put('me', data)
                    .then((response) => {
                        this.userData = response.data;
                    })
                    .catch((error) => {
                        if (error?.response?.status === 422) {
                            this.$router.push({ path: '/login' })
                            this.toast.error('Необходимо войти в аккаунт')
                        }else {

                            this.toast.error(handleError(error, 'При обновлении профиля произошла ошибка').message)
                        }
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
            return this.userData.first_name !== this.firstName || this.userData.last_name !== this.lastName
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';
@use '@/assets/styles/breakpoints';

.profile-container {
    display: flex;
    flex-direction: column;

    .user-info-container {
        display: grid;
        gap: 10px;
        grid-template-columns: 200px 1fr;

        @include breakpoints.lg(true) {
            grid-template-columns: 1fr;

        }

        .user-pic {
            aspect-ratio: 1;
            position: relative;
            border-radius: 7px;

            &.empty {
                @include helpers.flex-center;

                overflow: hidden;
                border: 2px dashed transparent;

                @include themes.dark {
                    border-color: var(--main-card-border);
                }

                @include themes.light {
                    border-color: var(--color-text);
                }


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
            }

            .edit-area {
                transition: opacity .2s;
                @include helpers.flex-center;
                position: absolute;
                inset: 0;
                opacity: 0;
                isolation: isolate;

                .edit-area-text {
                    margin-top: 90px;
                    z-index: 2;
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

        .user-info {
            border-radius: 5px;
            display: grid;
            gap: 5px;
            padding-top: 5px;

            .fields {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;

                .formkit-inner:focus-within {
                    border-color: var(--purple-1);
                    box-shadow: 0 0 0 1px var(--purple-1);
                }

                .formkit-input {
                    color: var(--color-text);
                }
            }

            .buttons {
                // grid-column: 1 / -1;
                margin-top: auto;
                display: flex;
                gap: 5px;
                justify-content: right;

                .button {
                    @include helpers.flex-center;
                    border-radius: 10px;
                    padding: 5px;
                    background-color: var(--color-background-mute-4);
                    width: 40px;
                    height: 40px;

                    &.save {
                        @include themes.light {
                            svg {
                                color: var(--color-background-mute);
                            }
                        }

                        &.active {
                            background-color: var(--purple-1);

                            cursor: pointer;
                        }
                    }
                }
            }
        }
    }
}
</style>
