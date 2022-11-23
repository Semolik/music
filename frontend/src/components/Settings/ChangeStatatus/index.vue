<template>
    <div class="container">
        <div class="selector">
            <div class="text">
                <div class="content">
                    <template v-if="!is_history_route">
                        Изменить тип аккаунта на
                    </template>
                    <template v-else>
                        История запросов
                    </template>
                </div>
                <router-link :to="is_history_route ? base_route_path : history_route_path" class="my-requests"
                    v-if="has_requests">
                    <template v-if="is_history_route">
                        отправить запрос
                    </template>
                    <template v-else>
                        мои запросы
                    </template>
                </router-link>
            </div>
            <div class="items" v-if="!is_history_route">
                <div :class="['item',{active: active_role === Role.RadioStation},{disabled: userRole === Role.RadioStation}]"
                    @click="this.active_role = Role.RadioStation">
                    Радиостанцию
                </div>
                <div :class="['item',{active: active_role === Role.Musician}, {disabled: userRole === Role.Musician}]"
                    @click="this.active_role = Role.Musician">
                    Музыканта
                </div>
                <div :class="['item',{active: active_role === Role.User}, {disabled: userRole === Role.User}]"
                    @click="this.active_role = Role.User">
                    Пользователя
                </div>
            </div>
        </div>
        <router-view v-if="is_history_route" />
        <template v-else>
            <div class="info">
                В сообщении будут передано имя которое указано у ваc в настройках аккаунта
            </div>
            <div class="request-form">
                <textarea name="message" placeholder="Напишите зачем вам нужен этот статус" v-model="messageText" id="" cols="30" rows="10"></textarea>
            </div>
            <div class="line">
                <div :class="['button','files', {active: isFilesSelected}]">
                    <FontAwesomeIcon icon="fa-paperclip" />
                    <input type="file" :title="filesTitle" @change="changeFiles" multiple>
                </div>
                <div class='button remove' v-if="isFilesSelected" @click="removeFiles">
                    <FontAwesomeIcon icon="fa-xmark" />
                </div>
                <div v-for="(file,index) in files" class="file" @click="removeFile(file)" title="Нажмите чтобы удалить">
                    <div class="icon">
                        <template v-if="previews[index]">
                            <img :src="previews[index].base64" alt="">
                            <FontAwesomeIcon icon="fa-image" />
                        </template>
                        <FontAwesomeIcon icon="fa-file" v-else />
                    </div>
                    <div class="name">{{file.name}}</div>
                </div>
            </div>
            <div :class="['button', {active: buttonActive}, {preloader: 0 < uploadPercentage < 100}]"
                :style="{'--i': uploadPercentage}" @click="sendMessageToAdmins">Отправить
                сообщение</div>
        </template>
    </div>
</template>
<script>
import { useToast } from "vue-toastification";
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPaperclip, faXmark, faImage, faFile } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useMemoize } from '@vueuse/core';
import { useBase64 } from '@vueuse/core';
import handleError from '/src/composables/errors';
import { HTTP } from '/src/http-common.vue'
import { files } from '@formkit/inputs';
import { Role } from '/src/helpers/roles.js';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '/src/stores/auth';
library.add(faPaperclip, faXmark, faImage, faFile);

export default {
    setup() {
        const toast = useToast();
        const { userRole } = storeToRefs(useAuthStore());
        const memoizeBase64Image = useMemoize(useBase64, {
            getKey: (file, headers) => file.name,
        });
        return {
            toast,
            memoizeBase64Image,
            Role,
            userRole
        }
    },
    components: {
        FontAwesomeIcon
    },
    data() {
        return {
            messageText: '',
            files: [],
            previews: [],
            has_requests: false,
            is_history_route: false,
            base_route_path: '/lk/update-status',
            history_route_path: '/lk/update-status/history',
            active_role: this.userRole,
            uploadPercentage: 0,
        };
    },
    mounted() {
        this.is_history_route = (this.$route.fullPath === this.history_route_path);
        HTTP.get('has-change-role-requests')
            .then((response) => {
                this.has_requests = response.data;
            })
            .catch((error) => {
                console.log(handleError(error, 'При получении информации о том отправлял ли пользватель запросы на смену аккаунта произошла ошибка').message)
                this.has_requests = false;
            });
    },
    methods: {
        sendMessageToAdmins() {
            if (!this.buttonActive) {
                if (!this.is_selected) {
                    this.toast.error('Выберите тип аккаунта')
                    return
                }
                if (this.active_role === this.userRole) {
                    this.toast.error('Измените тип акканта на отличный от вашего')
                    return
                }
                this.toast.error('Сообщение не может быть пустым')
            } else {
                this.sendForm();
            }
        },
        changeFiles(event) {
            let files = event?.target?.files;
            this.files = files ? [...files] : [];
            this.generatePreview();
            var fileBuffer = new DataTransfer();
            event.target.files = fileBuffer.files;
        },
        removeFiles() {
            this.files = [];
        },
        removeFile(target) {
            this.files = [...this.files].filter(file => file !== target);
        },
        generatePreview() {
            let files = [...this.files];
            this.previews = new Array(null).fill(files.length);
            files.forEach(async (file, index) => {
                if (this.isImage(file)) {
                    let result_base64 = this.memoizeBase64Image(file);
                    this.previews[index] = result_base64;
                } else {
                    this.previews[index] = false;
                }
            });
        },
        clearForm() {
            this.messageText = '';
            this.musician_selected = false;
            this.radioStation_selected = false;
            this.files = [];
            this.images = [];
        },
        sendForm() {
            var formData = new FormData();
            if (this.files.length > 0) {
                this.files.forEach(file => {
                    formData.append('files', file);
                })
            }
            formData.append('message', this.messageText);
            formData.append('account_status', this.active_role);
            this.uploadPercentage = 0;
            HTTP.post('change-role', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                onUploadProgress: function (progressEvent) {
                    this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100));
                }.bind(this)
            })
                .then((response) => {
                    this.clearForm();
                    this.toast(response.data.detail);
                    this.has_requests = true;
                    this.uploadPercentage = 0;
                })
                .catch((error) => {
                    this.toast.error(handleError(error, 'При отправке сообщения произошла ошибка').message)

                });
        },
        isImage(file) {
            return file?.type.split('/')?.includes('image')
        }
    },
    computed: {
        is_selected() {
            return Boolean(this.active_role)
        },
        buttonActive() {
            return this.is_selected && this.active_role !== this.userRole && this.messageText
        },
        isFilesSelected() {
            return this.files.length > 0;
        },
        filesTitle() {
            return this.isFilesSelected ? [...this.files].map(file => file.name).join('\n') : 'Файл не выбран'
        },

    }
}

</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.container {
    display: flex;
    flex-direction: column;
    gap: 8px;

    .selector {
        display: flex;
        gap: 10px;
        flex-direction: column;
        width: 100%;
        @include helpers.flex-center;

        .text {
            font-size: large;
            display: flex;
            width: 100%;
            position: relative;

            @include breakpoints.md(true) {
                flex-direction: column-reverse;
            }

            .content {
                flex-grow: 1;
                text-align: center;
                padding: 5px;
            }

            .my-requests {
                @include breakpoints.md {
                    position: absolute;
                    width: min-content;
                    white-space: nowrap;
                    right: 0;
                }

                font-size: initial;
                cursor: pointer;
                text-decoration: none;
                color: var(--color-text);
                text-align: center;
                background-color: var(--color-background-mute-3);
                border-radius: 10px;
                padding: 5px 10px;

                &:hover {
                    background-color: var(--color-background-mute-4);
                }
            }
        }

        .items {
            display: flex;

            flex-wrap: wrap;

            gap: 5px;
            width: 100%;
            border-radius: 5px;

            .item {
                cursor: pointer;
                text-align: center;
                flex-grow: 1;
                padding: 5px 40px;
                border-radius: 10px;
                background-color: var(--color-background-mute-3);

                &:not(:where(.active, .disabled)):hover {
                    background-color: var(--color-background-mute-4);
                }

                &.active {
                    cursor: auto;
                    background-color: var(--purple);
                }

                &.disabled {
                    cursor: not-allowed;
                    position: relative;
                    isolation: isolate;
                    background-color: transparent;
                    overflow: hidden;

                    &.active {
                        &::after {
                            opacity: 1;
                        }
                    }

                    &::after {
                        z-index: -1;
                        content: '';
                        background-color: var(--red-0);
                        opacity: 0.5;
                        position: absolute;
                        inset: 0;
                    }
                }
            }
        }
    }

    .info {
        background-color: var(--color-background-mute-4);
        padding: 5px;
        border-radius: 10px;
        text-align: center;
    }

    .request-form {
        display: flex;


        textarea {
            width: 100%;
            resize: none;
            border: none;
            outline: 1px solid var(--color-background-mute-6);
            background-color: transparent;
            border-radius: 5px;
            padding: 10px;
            color: var(--color-text);
            font-size: 1.1em;

            &:focus {
                outline: 1px solid var(--purple-1);
            }
        }
    }

    .line {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;

        .button {
            aspect-ratio: 1;
            @include helpers.flex-center;
            width: min-content;
            height: min-content;
            cursor: pointer;

            &.files {
                position: relative;

                input {
                    position: absolute;
                    inset: 0;
                    opacity: 0;
                    cursor: pointer;

                    &.hidden {
                        display: none;
                    }
                }
            }

            &.remove {
                background-color: var(--red-0);

                &:hover {
                    background-color: var(--red-0);
                }
            }
        }

        .file {
            background-color: var(--color-background-mute-3);
            border-radius: 10px;
            padding: 5px;
            cursor: pointer;

            gap: 5px;
            flex-grow: 1;
            display: flex;
            text-align: center;

            .icon {
                width: 50px;
                height: 50px;
                position: relative;
                background-color: var(--color-background-mute-4);
                border-radius: 10px;
                @include helpers.flex-center;

                svg {
                    width: 30px;
                    height: 30px;
                }

                img {
                    position: absolute;
                    inset: 0;
                    width: 50px;
                    height: 50px;
                    object-fit: cover;
                    border-radius: 10px;
                }
            }



            &:hover {
                background-color: var(--red-0);
            }

            .name {
                @include helpers.flex-center;
                overflow-wrap: anywhere;
                white-space: break-spaces;
                text-align: center;
            }
        }
    }

    .button {
        width: 100%;
        user-select: none;
        background-color: var(--color-background-mute-3);
        border-radius: 10px;
        padding: 10px;
        text-align: center;

        &.preloader {
            position: relative;
            isolation: isolate;
            overflow: hidden;

            &::after {
                z-index: -1;
                position: absolute;
                content: '';
                left: 0;
                top: 0;
                height: 100%;
                background-color: var(--red-0);
                width: calc(1% * var(--i));
            }
        }

        &:not(.active):hover {
            background-color: var(--color-background-mute-4);
        }

        &.active {
            cursor: pointer;
            background-color: var(--purple);
        }

        svg {
            width: 18px;
            height: 18px;
        }
    }
}
</style>
