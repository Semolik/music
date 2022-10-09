<template>
    <div class="selector">
        <div class="text">Изменить тип аккаунта на</div>
        <div class="items">
            <div class="item active">Радиостанцию</div>
            <div class="item">Музыканта</div>
        </div>
    </div>
</template>
<script setup>
import { isRadioStation, isMusician } from '../composables/roleChecker';

</script>
<style lang="scss">
@use '@/assets/styles/helpers';

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
        padding: 5px;
        border-radius: 5px;

        .item {
            text-align: center;
            flex-grow: 1;
            padding: 5px;
            border-radius: 15px;
            background-color: var(--color-background-mute-3);

            &.active {
                background-color: var(--purple);
            }
        }
    }
}
</style>
