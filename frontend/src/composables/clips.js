import { HTTP } from '/src/http-common.vue';
import { ref, computed } from 'vue';
const { VITE_CLIP_PAGE_COUNT } = import.meta.env;
const pageLimit = Number(VITE_CLIP_PAGE_COUNT);

export const useClipsGetter = (musician_id, loadOnUse = true, my = false) => {
    var page = ref(0);
    var buttonShowed = ref(true);
    var clips = ref([]);
    const getNextPage = async () => {
        page.value++;
        const { data } = await HTTP.get("clips" + (my ? "/my" : ""), { params: { musician_id: musician_id, page: page.value } });
        clips.value = [...clips.value, ...data];
        if (data.length < pageLimit) {
            buttonShowed.value = false
        }
    }
    const isbuttonShowed = computed(() => buttonShowed.value);
    if (loadOnUse) {
        getNextPage();
    }
    return { getNextPage, clips, isbuttonShowed }
}