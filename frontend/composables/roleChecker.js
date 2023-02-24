import { storeToRefs } from "pinia";
import { useAuthStore } from "../stores/auth";
import { Role } from "../helpers/roles.js";
import { computed } from "vue";

const { userRole } = storeToRefs(useAuthStore());

const isAdmin = computed(() => userRole.value === Role.Admin);
const isUser = computed(() => userRole.value === Role.User);
const isRadioStation = computed(() => userRole.value === Role.RadioStation);
const isMusician = computed(() => userRole.value === Role.Musician);

export { isAdmin, isUser, isRadioStation, isMusician };
