const useFullName = (userData) => {
    let name = [userData.first_name, userData.last_name].join(" ");
    if (name.trim() === "") {
        name = userData.username;
    }
    return name;
};
const useLoginValidation = (login) => {
    const regex = /[^a-zA-Z0-9_]/g;

    const error = regex.test(login)
        ? "Логин может содержать только латинские буквы, цифры и нижнее подчеркивание"
        : null;
    return {
        login: login.replace(regex, ""),
        error: error,
    };
};
const useEmailValidation = (email) => {
    const regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g;
    const error = regex.test(email) ? "Некорректный email" : null;
    return {
        email: email.replace(regex, ""),
        error: error,
    };
};
export { useFullName, useLoginValidation, useEmailValidation };
