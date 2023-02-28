const HandleAxiosError = (error, errorText) => {
    if (error.response) {
        let status = error.response.status;
        let message = error.response.data?.detail || errorText || error.message;
        return {
            message: Array.isArray(message)
                ? message.map((message) => message.msg).join("\n")
                : message,
            status: status,
        };
    } else if (error.request) {
        return {
            message: "Сервер не ответил на запрос",
            status: null,
        };
    } else {
        return {
            message: "Произошла ошибка",
            status: null,
        };
    }
};
const HandleOpenApiError = (error, errorText) => {
    if (error.body) {
        let message = error.body?.detail || errorText;
        if (message) {
            return {
                message: message,
                status: error.status,
            };
        }
    } else if (error.request) {
        return {
            message: "Сервер не ответил на запрос",
            status: null,
        };
    } else if (error.request) {
        if (error.request.errors) {
            const statusCodes = Object.keys(error.request.errors);
            if (statusCodes.includes("401")) {
                return {
                    message: "Неверный логин или пароль",
                    status: 401,
                };
            }
            return {
                message: error.request.errors[statusCodes[0]],
                status: statusCodes[0],
            };
        }
    }
    return {
        message: "Произошла ошибка",
        status: null,
    };
};
export { HandleAxiosError, HandleOpenApiError };
