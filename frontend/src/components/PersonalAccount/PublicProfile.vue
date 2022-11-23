<template>
    <div class="profile-container">
        <form class="user-info-container" @submit.prevent="formSubmited" ref="form">
            <SelectImage @changed="updatePic" :pictureUrl="picture" name="userPublicPicture" ref="selectPic" />
            <div class="button remove-picture" v-if="!avatarIsEmpty" @click="detelePicture">
                <FontAwesomeIcon icon="fa-trash" />
            </div>
            <div class="user-info">
                <FormField :borderRadius="10" name="name" label="Отображаемое имя" placeholder="Ваше имя" v-model="name"
                    offMargin notEmpty>
                    <span :class="['count', { wrong: nameLenghtLimit < 0 }]" v-if="nameLenghtLimit">
                        {{ nameLenghtLimit }}
                    </span>
                </FormField>
                <FormTextArea class="description" :borderRadius="10" label="Описание профиля"
                    placeholder="Напишите о себе" v-model="description" :rows="5" :paddingRight="20"
                    :maxLength="VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH">
                    <span :class="['count', { wrong: descriptionLenghtLimit < 0 }]" v-if="descriptionLenghtLimit">
                        {{ descriptionLenghtLimit }}
                    </span>
                </FormTextArea>
            </div>
            <div class="buttons">
                <FormField placeholder="id канала" v-model="yt" :borderRadius="10" offMargin class="iconed youtube"
                    offChangeColor>
                    <template v-slot:right>
                        <div class="icon">
                            <FontAwesomeIcon :icon="['fab', 'youtube']" />
                        </div>
                    </template>
                    <span :class="['count', { wrong: ytLenghtLimit < 0 }]" v-if="yt?.length">
                        {{ ytLenghtLimit }}
                    </span>
                </FormField>
                <FormField :borderRadius="10" v-model="telegram" offMargin placeholder="username"
                    class="iconed telegram" offChangeColor>
                    <template v-slot:right>
                        <div class="icon">
                            <FontAwesomeIcon :icon="['fab', 'telegram']" />
                        </div>
                    </template>
                    <span :class="['count', { wrong: telegramLenghtLimit < 0 }]" v-if="telegram?.length">
                        {{ telegramLenghtLimit }}
                    </span>
                </FormField>
                <FormField v-model="vk" :borderRadius="10" offMargin placeholder="username" class="iconed vk"
                    offChangeColor>
                    <template v-slot:right>
                        <div class="icon">
                            <FontAwesomeIcon :icon="['fab', 'vk']" />
                        </div>
                    </template>
                    <span :class="['count', { wrong: vkLenghtLimit < 0 }]" v-if="vk?.length">
                        {{ vkLenghtLimit }}
                    </span>
                </FormField>
                <div :class="['button', 'save', { active: dataChanged }, { wrong: fieldsWrong }]" @click="save">
                    <FontAwesomeIcon icon="fa-floppy-disk" />
                </div>
            </div>
        </form>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faYoutube, faTelegram, faVk } from '@fortawesome/free-brands-svg-icons';
import { faUser, faFloppyDisk, faTrash, faImage } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import handleError from '/src/composables/errors';
import { useToast } from "vue-toastification";
import FormField from '/src/components/FormField.vue';
import AnimateInteger from '/src/components/AnimateInteger.vue';
import SelectImage from '/src/components/SelectImage.vue';
import FormTextArea from '/src/components/FormTextArea.vue';
import { HTTP } from '/src/http-common.vue';

library.add(faUser, faFloppyDisk, faTrash, faImage, faYoutube, faTelegram, faVk);

export default {
    setup() {
        const toast = useToast();
        const { VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH, VITE_MAX_TELEGRAM_USERNAME_LENGTH, VITE_MAX_VK_USERNAME_LENGTH, VITE_MAX_YOUTUBE_ID_LENGTH, VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH } = import.meta.env;
        return {
            toast,
            VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH,
            VITE_MAX_TELEGRAM_USERNAME_LENGTH,
            VITE_MAX_VK_USERNAME_LENGTH,
            VITE_MAX_YOUTUBE_ID_LENGTH,
            VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH
        }
    },
    data() {
        return {
            userData: null,
            name: '',
            description: '',
            mounted: false,
            remove_picture: false,
            original_image: null,
            file_changed: false,
            fileChanged: false,
            picture: null,
            telegram: '',
            vk: '',
            yt: '',
        }
    },
    mounted() {
        this.mounted = true;
        HTTP.get('/me/public')
            .then(response => {

                this.setData(response.data);
            })
            .catch(error => {
                this.toast.error(handleError(error, 'При обновлении профиля произошла ошибка').message)
            })
    },
    components: {
        FontAwesomeIcon,
        FormField,
        AnimateInteger,
        SelectImage,
        FormTextArea
    },
    methods: {
        detelePicture() {
            this.$refs.selectPic.detelePicture();
            this.remove_picture = true;
            this.file_changed = true;
        },
        setData(data) {
            this.userData = data;
            const { name, description, links, picture } = data;
            this.name = name;
            this.description = description;
            this.vk = links.vk;
            this.telegram = links.telegram;
            this.yt = links.youtube;
            this.picture = picture;
        },
        updatePic(target) {
            this.file_changed = true;
            if (!this.file_changed) return
            let file = target.files;
            this.fileChanged = file !== this.userData.picture;
        },
        save() {
            if (this.dataChanged) {
                const { name, description, telegram, vk, yt, remove_picture } = this;
                const form = this.$refs.form;
                let data = new FormData(form);
                data.append('name', name);
                data.append('description', description);
                data.append('telegram', telegram || '');
                data.append('vk', vk || '');
                data.append('youtube', yt || '');
                data.append('remove_picture', remove_picture);
                HTTP.put('/me/public', data)
                    .then((response) => {
                        this.remove_picture = false;
                        this.file_changed = false;
                        this.setData(response.data);
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
            let links = this.userData.links;
            return (
                this.userData.name !== this.name ||
                this.userData.description !== this.description ||
                this.file_changed || this.vk !== links.vk ||
                this.yt !== links.youtube ||
                this.telegram !== links.telegram
            )
        },
        fieldsWrong() {
            return this.nameWrong || this.telegramWrong || this.vkWrong || this.ytWrong || this.descriptionWrong
        },
        nameWrong() {
            return this.nameLenghtLimit < 0 || this.name?.length === 0
        },
        descriptionWrong() {
            return this.descriptionLenghtLimit < 0
        },
        telegramWrong() {
            return this.telegramLenghtLimit < 0
        },
        vkWrong() {
            return this.vkLenghtLimit < 0
        },
        ytWrong() {
            return this.ytLenghtLimit < 0
        },
        nameLenghtLimit() {
            let lenght = this.name?.length;
            if (!lenght) return
            return this.VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH - lenght
        },
        descriptionLenghtLimit() {
            let lenght = this.description?.length;
            if (!lenght) return
            return this.VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH - lenght
        },
        telegramLenghtLimit() {
            let lenght = this.telegram?.length;
            if (!lenght) return
            return this.VITE_MAX_TELEGRAM_USERNAME_LENGTH - lenght
        },
        vkLenghtLimit() {
            let lenght = this.vk?.length;
            if (!lenght) return
            return this.VITE_MAX_VK_USERNAME_LENGTH - lenght
        },
        ytLenghtLimit() {
            let lenght = this.yt?.length;
            if (!lenght) return
            return this.VITE_MAX_YOUTUBE_ID_LENGTH - lenght
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.profile-container {
    display: flex;
    flex-direction: column;

    .user-info-container {
        display: grid;
        gap: 10px;
        grid-template-columns: 210px 1fr;

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

            @include breakpoints.lg(true) {
                grid-column: 1 / -1;
            }
        }

        .buttons {
            margin-top: auto;
            display: flex;
            gap: 10px;

            @include breakpoints.xl(true) {
                flex-wrap: wrap;
            }

            grid-column: 1 / -1;

            .iconed {
                &.youtube {
                    --icon-color: red;
                }

                &.vk {
                    --icon-color: #0077FF;
                }

                &.telegram {
                    --icon-color: #0088cc;
                }

                svg {
                    transition: color .2s;
                }

                :focus-within {
                    svg {
                        color: var(--icon-color);
                    }
                }
            }

            .button {
                cursor: auto;
                @include helpers.flex-center;
                border-radius: 10px;
                padding: 5px;
                background-color: var(--color-background-mute-4);
                min-width: 40px;
                min-height: 40px;


                @include breakpoints.xl(true) {
                    width: 100%;
                }

                &.save {

                    &.wrong {
                        background-color: var(--red-0);
                    }

                    &.active {
                        background-color: var(--purple-1);
                        cursor: pointer;
                    }
                }
            }

            .formkit-outer {
                width: 100%;
            }
        }

        .user-info {
            border-radius: 5px;
            display: grid;
            grid-template-rows: min-content min-content;
            gap: 10px;
            padding-top: 5px;

            .description {
                position: relative;

                .count {
                    position: absolute;
                    right: 0px;
                    bottom: 8px;
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
