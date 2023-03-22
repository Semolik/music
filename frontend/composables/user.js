const useFullName = (userData) => {
    let name = [userData.first_name, userData.last_name].join(" ");
    if (name.trim() === "") {
        name = userData.username;
    }
    return name;
};

export { useFullName };
