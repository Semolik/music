module.exports = {
    apps: [
        {
            name: "semolik-music-frontend",
            port: "4000",
            exec_mode: "cluster",
            instances: "max",
            script: "./.output/server/index.mjs",
        },
    ],
};
