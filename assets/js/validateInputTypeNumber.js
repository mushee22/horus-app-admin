function validateFloatInput(input) {
    input.value = input.value.replace(/[^0-9.]/g, '');

    if ((input.value.match(/\./g) || []).length > 1) {
        input.value = input.value.slice(0, -1);
    }
}