<template>
    <div class="selector">
        <div class="item active">
            на рассмотрении
            <div class="bg in-progress"></div>
        </div>
        <div class="item">
            одобренные
            <div class="bg successfully"></div>
        </div>
        <div class="item">
            отклоненные
            <div class="bg rejected"></div>
        </div>
    </div>
</template>
<script>
export default {

}
</script>
<style lang="scss">
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
        background-color: var(--color-background-mute-3);
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
        }
    }
}
</style>