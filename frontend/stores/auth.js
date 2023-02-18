import { defineStore } from "pinia";

export const useSearchStore = defineStore({
    id: "search",
    state: () => ({
        query: "",
        active: false,
        category: "all",
    }),
    actions: {
        setQuery(query) {
            this.query = query;
        },
    },
});
