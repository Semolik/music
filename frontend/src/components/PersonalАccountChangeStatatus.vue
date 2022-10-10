<template>
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
        <FormKitTextArea :name="" label="Предоставьте информацию о себе"></FormKitTextArea>
    </div>
</template>
<script>
import { isRadioStation, isMusician } from '../composables/roleChecker';
import FormKitTextArea from './FormKitTextArea.vue';
export default {
    data() {
        return {
            radioStation_selected: isRadioStation.value,
            musician_selected: isMusician.value,
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
        }
    },
    components: { FormKitTextArea }
}

</script>
<style lang="scss" scoped>
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


}
</style>
