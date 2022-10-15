<template>
    <div class="request">
        <div :class="['line', {adminMode: adminMode}]">
            <div class="date">{{request.time_created}}</div>
            <div :class="['status', request.status]" v-if="!hideStatus"></div>
            <template v-if="adminMode">
                <div class="block full-name" v-if="fullName" @click="modalOpened = true">
                    {{fullName}}
                </div>
                <div class="user-modal-container" v-if="modalOpened">
                    <div class="user-modal-wrapper" @click.self="modalOpened = false">
                        <div class="content">
                            <img :src="request.user.picture" alt="" v-if="request.user.picture">
                            <div class="blocks">
                                <div class="block">
                                    id: {{request.user.id}}
                                </div>
                                <div class="block" v-if="firstName">
                                    имя: {{firstName}}
                                </div>
                                <div class="block" v-if="lastName">
                                    фамилия: {{lastName}}
                                </div>
                                <div class="block">
                                    юзернейм: {{request.user.username}}
                                </div>
                                <div class="block" v-if="accountStatus">
                                    статус: {{accountStatus}}
                                </div>
                            </div>
                            <div class="button" @click="modalOpened = false">закрыть</div>
                        </div>
                    </div>
                </div>
            </template>
        </div>
        <div class="message">{{request.message}}</div>
        <div class="files" v-if="!isFilesEmpty">
            <FileBlock :file="file" v-for="file in request.files" />
        </div>
        <div class="buttons" v-if="adminMode">
            <div class="button" @click="openTextArea = !openTextArea">
                <span v-if="!openTextArea">ответить</span>
                <span v-else>закрыть</span>
            </div>
        </div>
        <template v-if="openTextArea">
            <textarea name="message" v-model="answerMessageText" id="" cols="30" rows="10"></textarea>
            <div class="buttons">
                <div class="button">
                    отправить
                </div>
            </div>
        </template>
    </div>
</template>
<script>
import FileBlock from "./FileBlock.vue";


export default {
    props: {
        request: Object,
        adminMode: Boolean,
        hideStatus: Boolean,
    },

    data() {
        return {
            modalOpened: false,
            openTextArea: false,
            answerMessageText: '',
        }
    },
    components: { FileBlock },
    computed: {
        isFilesEmpty() {
            return !this.request.files || this.request.files.length === 0
        },
        fullName() {
            let user = this.request?.user;
            if (!user) return
            let fullNameChapters = [user.first_name, user.last_name].filter(Boolean);
            if (fullNameChapters.length === 0) return
            return fullNameChapters.join(' ')
        },
        firstName() {
            let user = this.request?.user;
            if (!user || !user.first_name) return
            return user.first_name
        },
        lastName() {
            let user = this.request?.user;
            if (!user || !user.last_name) return
            return user.last_name
        },
        accountStatus() {
            let user = this.request?.user;
            if (!user) return
            if (user.is_superuser) {
                return 'администратор'
            }
            if (user.is_musician) {
                return 'музыкант'
            }
            if (user.is_radio_station) {
                return 'радиостанция'
            }
            return 'пользователь';
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/helpers';
@use '@/assets/styles/themes';

.request {
    background-color: var(--color-background-mute-3);
    padding: 10px;
    border-radius: 15px;
    gap: 8px;
    display: flex;
    flex-direction: column;

    .line {
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 5px;

        &.adminMode {
            justify-content: normal;
        }

        .block,
        .status,
        .date {
            padding: 3px 10px;
            text-align: center;
            background-color: var(--color-background-mute-4);
            border-radius: 10px;

            @include breakpoints.md(true) {
                padding: 3px 40px;
                flex-grow: 1;
            }
        }

        .full-name {
            cursor: pointer;
            user-select: none;

            &:hover {
                background-color: var(--color-background-mute-5);
            }
        }

        .user-modal-container {
            position: absolute;
            inset: 0;
            z-index: 99;
            backdrop-filter: blur(10px);

            .user-modal-wrapper {
                width: 100%;
                height: 100%;
                @include helpers.flex-center;
                position: relative;
                isolation: isolate;


                &::after {
                    content: '';
                    position: absolute;
                    inset: 0;
                    z-index: 1;
                    background-color: var(--color-background-mute);
                    opacity: 0.5;
                }

                .content {
                    z-index: 2;
                    background-color: var(--color-background-mute-2);
                    padding: 10px;
                    max-width: 400px;
                    width: 100%;
                    display: flex;
                    flex-direction: column;
                    border-radius: 20px;
                    gap: 5px;

                    @include themes.light {
                        box-shadow: var(--main-card-shadow);
                    }

                    img {
                        object-fit: cover;
                        width: 100%;
                        border-radius: 10px;
                    }

                    .blocks {
                        display: flex;
                        flex-direction: column;
                        gap: 4px;

                        .block {
                            padding: 10px;
                        }
                    }

                    .button {
                        background-color: black;
                        color: white;
                        width: 100%;
                        text-align: center;
                        padding: 10px;
                        border-radius: 10px;
                        cursor: pointer;
                    }
                }
            }
        }

        .status {
            &.in-progress {
                background-color: var(--purple);

                &::after {
                    content: 'на рассмотрении';
                }
            }

            &.successfully {
                background-color: var(--green-128);

                &::after {
                    content: 'одобрено';
                }
            }

            &.rejected {
                background-color: var(--red-0);

                &::after {
                    content: 'отклонено';
                }
            }
        }
    }

    .message {
        background-color: var(--color-background-mute-4);
        padding: 10px;
        border-radius: 10px;
    }

    .files {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
    }

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

    .buttons {
        display: flex;
        gap: 5px;
        justify-content: right;

        .button {
            user-select: none;
            cursor: pointer;
            background-color: var(--color-background-mute-5);
            padding: 5px 10px;
            border-radius: 10px;

            &:hover {
                background-color: var(--color-background-mute-6);
            }
        }
    }
}
</style>