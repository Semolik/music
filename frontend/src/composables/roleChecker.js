import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth';
import { Role } from '../helpers/roles.js';
import { computed } from 'vue';

const { userRole } = storeToRefs(useAuthStore());

const isAdmin = computed(() => userRole === Role.Admin);
const isUser = computed(() => userRole === Role.User);
const isRadioStation = computed(() => userRole === Role.RadioStation);
const isMusician = computed(() => userRole === Role.Musician);

export { isAdmin, isUser, isRadioStation, isMusician };
