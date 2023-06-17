<template>
    <FormContainer
        headline="Востановление пароля"
        max-width="500px"
        ref="formContainer"
        :description="
            requestId
                ? null
                : 'Если вы забыли пароль, то введите свой никнейм и напишите сообщение для администрации'
        "
    >
        <reset-password
            v-model:requestId="requestId"
            :formContainer="formContainer"
        />
    </FormContainer>
</template>
<script setup>
const formContainer = ref(null);
const requestId = useLocalStorage("reset-password-request-id", null);
</script>
