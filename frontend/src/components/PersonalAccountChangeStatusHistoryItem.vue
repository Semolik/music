<template>
    <div class="request">
        <div class="line">
            <div class="date">{{request.time_created}}</div>
            <div :class="['status', request.status]"></div>
        </div>
        <div class="message">{{request.message}}</div>
        <div class="files" v-if="!isFilesEmpty">
            <FileBlock :file="file" v-for="file in request.files" />
        </div>
    </div>
</template>
<script>
import FileBlock from "./FileBlock.vue";

export default {
    props: {
        request: Object
    },
    components: { FileBlock },
    computed: {
        isFilesEmpty() {
            return !this.request.files || this.request.files.length === 0
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';

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
}
</style>