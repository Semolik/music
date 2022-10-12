<template>
    <div class="container">
        <div class="selector">
            <div class="text">Изменить тип аккаунта на</div>
            <div class="items">
                <div :class="['item',{active: radioStation_selected}]" @click="selectRadioStation">
                    Радиостанцию
                </div>
                <div :class="['item',{active: musician_selected}]" @click="selectMusician">
                    Музыканта
                </div>
            </div>
        </div>
        <div class="info">
            В сообщении будут передано имя которое указано у ваc в настройках аккаунта
        </div>
        <div class="request-form">
            <textarea v-model="messageText" id="" cols="30" rows="10"></textarea>
        </div>
        <div class="line" v-auto-animate>
            <div :class="['button','files', {active: isFilesSelected}]">
                <FontAwesomeIcon icon="fa-paperclip" />
                <input type="file" @change="changeFiles" multiple>
            </div>
            <div class='button remove' v-if="isFilesSelected" @click="removeFiles">
                <FontAwesomeIcon icon="fa-xmark" />
            </div>
            <div v-for="file in files" class="file" @click="removeFile(file)">{{file.name}}</div>
        </div>
        <div :class="['button', {active: buttonActive}]" @click="sendMessageToAdmins">Отправить сообщение</div>
    </div>
</template>
<script>
import { isRadioStation, isMusician } from '../composables/roleChecker';
import { useToast } from "vue-toastification";
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPaperclip, faXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faPaperclip, faXmark);

export default {
    setup() {
        const toast = useToast();
        return {
            toast
        }
    },
    components: {
        FontAwesomeIcon
    },
    data() {
        return {
            radioStation_selected: isRadioStation.value,
            musician_selected: isMusician.value,
            messageText: '',
            files: []
        };
    },
    methods: {
        selectRadioStation() {
            this.radioStation_selected = true;
            this.musician_selected = false;
        },
        selectMusician() {
            this.musician_selected = true;
            this.radioStation_selected = false;
        },
        sendMessageToAdmins() {
            if (!this.buttonActive) {
                if (!this.is_selected) {
                    this.toast.error('Выберите тип аккаунта')
                    return
                }
                this.toast.error('Сообщение не может быть пустым')
            }
        },
        changeFiles(event) {
            this.files = event?.target?.files || [];
        },
        removeFiles() {
            this.files = [];
        },
        removeFile(target) {
            this.files = [...this.files].filter(file => file !== target);
        }
    },
    computed: {
        is_selected() {
            return this.musician_selected || this.radioStation_selected
        },
        buttonActive() {
            return this.is_selected && this.messageText
        },
        isFilesSelected() {
            return this.files.length > 0;
        }
    }
}

</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';

.container {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .selector {
        display: flex;
        gap: 10px;
        flex-direction: column;
        width: 100%;
        @include helpers.flex-center;

        .text {
            font-size: large;
        }

        .items {
            display: flex;
            gap: 5px;
            width: 100%;
            border-radius: 5px;

            .item {
                cursor: pointer;
                text-align: center;
                flex-grow: 1;
                padding: 5px;
                border-radius: 15px;
                background-color: var(--color-background-mute-3);

                &:not(.active):hover {
                    background-color: var(--color-background-mute-4);
                }

                &.active {
                    cursor: auto;
                    background-color: var(--purple);
                }

                &.disabled {
                    cursor: not-allowed;
                    background-color: var(--red-0);
                }
            }
        }
    }

    .info {
        background-color: var(--color-background-mute-4);
        padding: 5px;
        border-radius: 15px;
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
            border-radius: 15px;
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
            cursor: pointer;

            &.files {
                position: relative;

                input {
                    position: absolute;
                    inset: 0;
                    opacity: 0;
                }
            }

            &.remove {
                background-color: var(--red-0);
            }
        }

        .file {
            background-color: var(--color-background-mute-3);
            border-radius: 15px;
            padding: 10px;
            cursor: pointer;
            white-space: nowrap;
        }
    }

    .button {
        width: 100%;
        user-select: none;
        background-color: var(--color-background-mute-3);
        border-radius: 15px;
        padding: 10px;
        text-align: center;

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
