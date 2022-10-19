<template>
    <div class="musician-cabinet-container">
        <div class="buttons">
            <div class="button">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-plus" />
                </div>
                <div class="text">Загрузить</div>
            </div>
            <div class="button">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-music" />
                </div>
                <div class="text">Плейлисты</div>
            </div>
        </div>
        <FormField placeholder="Поиск" borderRadius="10"></FormField>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus, faMusic } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import FormField from './FormField.vue';
library.add(faPlus, faMusic);
export default {
    components: {
        FontAwesomeIcon,
        FormField
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.musician-cabinet-container {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .buttons {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;

        .button {
            display: flex;
            flex-direction: column;
            background-color: var(--color-background-mute-3);
            padding: 10px;
            gap: 5px;
            border-radius: 15px;
            cursor: pointer;

            &:hover {
                background-color: var(--color-background-mute-4);
            }

            .icon {
                @include helpers.flex-center;

                svg {
                    height: 25px;
                }
            }

            .text {
                text-align: center;
            }
        }
    }
}
</style>