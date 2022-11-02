export default function (error, errorText) {
    if (error.response) {
        let status = error.response.status;
        let message = error.response.data?.detail || (errorText || error.message);
        return {
            message: Array.isArray(message) ? message.map(message => message.msg).join('\n') : message,
            status: status,
        }
    } else if (error.request) {
        return {
            message: 'Запрос был сделан, но ответ не получен',
            status: null,
        }
    } else {
        return {
            message: 'Произошла ошибка',
            status: null,
        }
    }
}