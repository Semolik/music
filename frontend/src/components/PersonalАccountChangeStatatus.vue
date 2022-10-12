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
        <div class="request-form">
            <textarea v-model="messageText" id="" cols="30" rows="10"></textarea>
        </div>
        <div :class="['button', {active: buttonActive}]" @click="sendMessageToAdmins">Отправить сообщение</div>
    </div>
</template>
<script>
import { isRadioStation, isMusician } from '../composables/roleChecker';
import { useToast } from "vue-toastification";

export default {
    setup() {
        const toast = useToast();
        return {
            toast
        }
    },
    data() {
        return {
            radioStation_selected: isRadioStation.value,
            musician_selected: isMusician.value,
            messageText: '',
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
        }
    },
    computed: {
        is_selected() {
            return this.musician_selected || this.radioStation_selected
        },
        buttonActive() {
            return this.is_selected && this.messageText
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
            padding: 5px 0px;
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
    }
}
</style>
