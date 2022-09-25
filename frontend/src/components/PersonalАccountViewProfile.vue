<template>
    <div class="profile-container">
        <div class="user-info-container">
            <div :class="['user-pic', {empty: avatarIsEmpty}]">
                <FontAwesomeIcon icon="fa-user" v-if="avatarIsEmpty" />
                <div class="edit-area">
                    <div class="edit-area-text">выбрать файл</div>
                    <input type="file">
                </div>
            </div>
            <div class="user-info">
                <h2>{{fullName}}</h2>
            </div>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth';
library.add(faUser)

export default {
    setup() {
        const { userData } = storeToRefs(useAuthStore());
        return {
            userData
        }
    },
    components: {
        FontAwesomeIcon,
    },
    computed: {
        avatarIsEmpty() {
            if (!this.userData) return true
            return !Boolean(this.userData.picture)
        },
        fullName() {
            if (!this.userData) return
            return [this.userData.first_name, this.userData.last_name].filter(Boolean).join(' ')
        }

    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.profile-container {
    display: flex;
    flex-direction: column;

    .user-info-container {
        display: grid;
        grid-template-columns: 250px 1fr;

        .user-pic {
            aspect-ratio: 1;
            position: relative;

            &.empty {
                @include helpers.flex-center;
                border-radius: 50%;
                margin: 15px;
                border: 2px dashed var(--main-card-border);
                overflow: hidden;

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
            padding: 10px;
            display: grid;
            gap: 5px;

            h2 {
                text-align: center;
            }
        }
    }
}
</style>
