<template>
    <div class="container">
        <div class="selector">
            <div :class="['item', {active: current===all}]" @click="current = all">
                все
                <div class="bg all"></div>
            </div>
            <div :class="['item', {active: current===in_progress}]" @click="current = in_progress">
                на рассмотрении
                <div class="bg in-progress"></div>
            </div>
            <div :class="['item', {active: current===successfully}]" @click="current = successfully">
                одобренные
                <div class="bg successfully"></div>
            </div>
            <div :class="['item', {active: current===rejected}]" @click="current = rejected">
                отклоненные
                <div class="bg rejected"></div>
            </div>
        </div>
        <div class="requests" v-if="!requestsEmpty">
            <status-history-item :adminMode="true" :ырщц="current!==all" :request="request"
                v-for="request in this.requests" />
        </div>
        <div class="empty" v-else>тут пусто</div>
        <div class="buttons" v-if="show_button && !loading">
            <div class="button" @click="getNextPage">Загрузить еще</div>
        </div>
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import StatusHistoryItem from './PersonalAccountChangeStatusHistoryItem.vue';
export default {
    data() {
        return {
            current: 'in-progress',
            in_progress: 'in-progress',
            successfully: 'successfully',
            rejected: 'rejected',
            all: 'all',
            page: 1,
            requests: [],
            loading: false,
            show_button: true,
        }
    },
    components: { StatusHistoryItem },
    watch: {
        current(value) {
            // this.loading = true;
            this.requests = [];
            this.page = 1;
            this.show_button = true;
            this.getPage();
        }
    },
    methods: {
        getPage() {
            this.loading = true;
            HTTP.get('change-role-requests', { params: { page: this.page, filter: this.current } })
                .then((response) => {
                    if (response.data.length === 0) {
                        this.show_button = false;
                    }
                    this.requests = [...this.requests, ...response.data]
                })
                .catch((error) => {
                }).finally(() => {
                    this.loading = false;
                });
        },
        getNextPage() {
            this.page++;
            this.getPage();
        }
    },
    mounted() {
        this.getPage();
    },
    computed: {
        requestsEmpty() {
            if (this.loading) return
            return this.requests.length === 0
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
        flex-wrap: wrap;
        gap: 5px;

        .item {
            overflow: hidden;
            border-radius: 15px;
            text-align: center;
            padding: 10px;
            flex-grow: 1;
            position: relative;
            isolation: isolate;

            &:not(.active) {
                cursor: pointer;

                &:hover {
                    .bg {
                        opacity: 0.5;
                    }
                }
            }

            &.active {
                .bg {
                    opacity: 1;
                }
            }

            .bg {
                transition: .2s opacity;
                position: absolute;
                inset: 0;
                opacity: 0.3;
                z-index: -1;

                &.in-progress {
                    background-color: var(--purple);
                }

                &.successfully {
                    background-color: var(--green-128);
                }

                &.rejected {
                    background-color: var(--red-0);
                }

                &.all {
                    background-color: var(--color-background-mute-6);
                }
            }
        }
    }

    .requests {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .empty {
        @include helpers.flex-center;
        border: 2px dashed var(--color-text);
        padding: 20px;
        border-radius: 15px;
    }

    .buttons {
        display: flex;
        justify-content: center;
        width: 100%;

        .button {
            background-color: var(--color-background-mute-4);
            padding: 10px 30px;
            border-radius: 15px;
            cursor: pointer;
        }
    }
}
</style>