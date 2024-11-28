function handleFormSubmit(event) {
    event.preventDefault(); 
    const formData = new FormData(event.target); 
    const actionUrl = event.target.action;

    console.log("Дані форми:", Object.fromEntries(formData));

    fetch(actionUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Помилка при надсиланні даних');
        }
    })
    .then(data => {
        console.log("Успіх:", data);
        
    })
    .catch(error => {
        console.error("Виникла помилка:", error);
    });
}

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', handleFormSubmit);
});

unction confirmDelete(id, type) {
    if (confirm("Ви впевнені, що хочете видалити цей запис?")) {
        fetch(`/${type}/${id}/delete`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                console.log("Запис видалено успішно.");
                location.reload(); 
            } else {
                throw new Error('Не вдалося видалити запис');
            }
        })
        .catch(error => {
            console.error("Виникла помилка:", error);
        });
    }
}

document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', () => {
        const id = button.dataset.id; // Отримуємо ID з data-атрибуту
        const type = button.dataset.type; // Отримуємо тип з data-атрибуту
        confirmDelete(id, type);
    });
});