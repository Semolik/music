<template>
    <date-picker v-model="date" is-dark mode="dateTime" is24hr>
        <template v-slot="{ inputValue, inputEvents }">
            <FormField class="calendar" :modelValue="inputValue" :inputEvents="inputEvents" label="Начало активности"
                :borderRadius="10" off-margin>
                <FontAwesomeIcon icon="fa-calendar" />
            </FormField>
        </template>
    </date-picker>
</template>
<script>
import { DatePicker } from 'v-calendar';
import FormField from './FormField.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCalendar } from '@fortawesome/free-solid-svg-icons';
library.add(faCalendar);
export default {
    props: { modelValue: Date },
    components: { DatePicker, FormField, FontAwesomeIcon },
    emits: ['update:modelValue'],
    data() {
        return {
            date: this.modelValue,
        }
    },
    watch: {
        date(value) {
            this.$emit('update:modelValue', value);
        }
    }
}
</script>
<style lang="scss">
.calendar {
    svg {
        padding: 10px;
    }
}
</style>