export default function (error) {
    if (error.response) {
        return {
            message: error.response.data?.message || error.message,
            status: error.response.status,
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