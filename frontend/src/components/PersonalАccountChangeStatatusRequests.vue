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
        <div class="requests">
            <status-history-item :adminMode="true" :hideStatus="current!==all" :request="request"
                v-for="request in this.requests" />
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
        }
    },
    components: { StatusHistoryItem },
    methods: {
        getPage() {
            this.loading = true;
            HTTP.get('change-role-requests', { params: { page: this.page } })
                .then((response) => {
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
    }
}
</script>
<style lang="scss" scoped>
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
}
</style>