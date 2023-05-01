import { defineStore } from "pinia";

interface Link {
    name: string;
    title: string;
}

export const useHeaderStore = defineStore({
    id: "header",
    state: () => ({
        title: "",
        links: [] as Link[],
        currentRouteName: "",
    }),
    getters: {
        isActive: (state) => () => {
            return (
                (state.title && state.title.length) || state.links.length > 0
            );
        },
    },
    actions: {
        reset() {
            this.title = "";
            this.links = [];
        },
        setTitle(title: string) {
            useHead({
                title: title,
            });
            this.title = title;
        },
    },
});
