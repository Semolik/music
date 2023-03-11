export const useTyping = (values, startText, typeTimeout = 800) => {
    const typingText = ref(startText);
    const typeText = (text) => {
        typingText.value = "";
        var currentIndex = 0;
        var reverse = false;
        var wait = false;
        setInterval(() => {
            if (!reverse && currentIndex < text.length) {
                typingText.value += text[currentIndex];
                currentIndex++;
            } else {
                wait = true;
                setTimeout(() => {
                    reverse = true;
                    wait = false;
                }, 1500);
            }
            if (reverse && currentIndex > 0) {
                typingText.value = typingText.value.slice(0, -1);
                currentIndex--;
            } else {
                clearInterval();
            }
        }, typeTimeout / text.length);
    };
    const getRandomValue = () => {
        return values[Math.floor(Math.random() * values.length)];
    };

    setTimeout(() => {
        const interval = setInterval(() => {
            if (typingText.value.length > 0) {
                typingText.value = typingText.value.slice(0, -1);
            } else {
                clearInterval(interval);
            }
        }, 100);
        setTimeout(() => {
            typeText(getRandomValue());
            setInterval(() => {
                typeText(getRandomValue());
            }, typeTimeout * 2 + 1500);
        }, typingText.value.length * 100 + 1000);
    }, 3000);
    return { typingText };
};
