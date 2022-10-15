<template>
    <div class="requests-container">
        <div class="request" v-for="request in requests">
            <div class="line">
                <div class="date">11.11.1111</div>
                <div :class="['status', request.status]"></div>
            </div>
            <div class="message">{{request.message}}</div>
            {{request.files}}
        </div>
        <div class="request">
            <div class="line">
                <div :class="['status', 'successfully']"></div>
            </div>
        </div>
        <div class="request">
            <div class="line">
                <div :class="['status', 'rejected']"></div>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
.requests-container {
    display: flex;
    flex-direction: column;
    gap: 5px;

    .request {
        background-color: var(--color-background-mute-3);
        padding: 10px;
        border-radius: 15px;
        gap: 10px;
        display: flex;
        flex-direction: column;

        .line {
            width: 100%;
            display: flex;

            .date {
                padding: 3px 0px;
            }

            .status {
                margin-left: auto;
                padding: 3px 10px;
                border-radius: 10px;

                &.in-progress {
                    background-color: var(--purple);

                    &::after {
                        content: 'на рассмотрении';
                    }
                }

                &.successfully {
                    background-color: var(--green-128);

                    &::after {
                        content: 'успешно';
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
    }
}
</style>
<script>
import { HTTP } from '../http-common.vue';

export default {
    data() {
        return {
            requests: []
        }
    },
    mounted() {
        HTTP.get('change-role')
            .then((response) => {
                this.requests = response.data;
            })
            .catch((error) => {
                this.requests = [];
            });
    }
}
</script>