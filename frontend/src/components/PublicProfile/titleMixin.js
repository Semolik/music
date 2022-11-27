export default {
    inject: ['publicProfileData'],
    mounted() {
        const { name } = this.publicProfileData;
        document.title = name;
    },
}