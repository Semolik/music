import { defineStore } from "pinia";

interface Link {
    name?: string;
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
            return !!(
                (state.title && state.title.length > 0) ||
                state.links.length > 0
            );
        },
    },
    actions: {
        reset() {
            this.links.length = 0;
            this.title = "";
        },
        setTitle(title: string) {
            console.log("setTitle", title);
            this.title = title;
            useHead({
                title: title,
            });
        },
    },
});
