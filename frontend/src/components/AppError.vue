<template>
    <FormContainer center>
        <div class="status">{{ StatusCode }}</div>
        <div class="message">{{ Message }}</div>
        <router-link to="/" class="buttton" @click="this.$emit('reset_error')">
            <font-awesome-icon icon="fa-solid fa-arrow-left-long" />
            <div class="text">Вернуться на главную</div>
        </router-link>
    </FormContainer>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faArrowLeftLong } from '@fortawesome/free-solid-svg-icons';
library.add(faArrowLeftLong);
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import FormContainer from './FormContainer.vue';
export default {
    components: { FontAwesomeIcon, FormContainer },
    props: {
        inputStatusCode: Number,
        inputMessage: String,
    },
    data() {
        return {
            defaultStatusCode: 404,
            defaultMessage: 'Страница не найдена',
        }
    },
    computed: {
        StatusCode() {
            return this.inputMessage !== undefined ? this.inputStatusCode : this.defaultStatusCode
        },
        Message() {
            return this.inputMessage || this.defaultMessage
        }
    }

}
</script>
<style scoped lang="scss">
@use '@/assets/styles/helpers';

.status {
    font-size: 120px;
}

.message {
    padding: 10px;
    font-size: 20px;
    text-align: center;
}

.buttton {
    @include helpers.flex-center;
    gap: 10px;
    text-decoration: none;
    color: var(--color-text);
    background-color: var(--color-background-mute-3);
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    transition: transform .2s, background-color .2s;

    .hoverable &:hover {
        background-color: var(--color-background-mute-2);
    }

    &:active {
        transform: scale(1.02);
    }
}

// }
</style>