<template>

</template>
<script>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth';
import { Role } from '../helpers/roles.js';
export default {
    setup() {
        const { userRole } = storeToRefs(useAuthStore());
        return {
            userRole
        }
    },
    computed: {
        isAdmin() {
            return this.userRole === Role.Admin;
        }
    }
}
</script>
<style lang="scss">

</style>
