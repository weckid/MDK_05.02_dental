// catalog.js
document.addEventListener('DOMContentLoaded', function() {
    // Фильтрация услуг
    const filterBtns = document.querySelectorAll('.filter-btn');
    const serviceCards = document.querySelectorAll('.service-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Убираем активный класс у всех кнопок
            filterBtns.forEach(b => b.classList.remove('active'));
            // Добавляем активный класс текущей кнопке
            this.classList.add('active');

            const filterValue = this.getAttribute('data-filter');

            serviceCards.forEach(card => {
                const category = card.getAttribute('data-category');

                if (filterValue === 'all' || category === filterValue) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });

    // Модальное окно
    const modal = document.getElementById('serviceModal');
    const closeModal = document.querySelector('.close-modal');
    const modalBody = document.getElementById('modal-body');
    const infoBtns = document.querySelectorAll('.service-btn.secondary');

    // Данные для модального окна
    const serviceDetails = {
        1: {
            title: "Лечение кариеса",
            description: "Кариес - это разрушение твердых тканей зуба под воздействием кислот, образующихся в результате жизнедеятельности бактерий. Наша клиника предлагает современное лечение кариеса с использованием инновационных материалов и технологий.",
            features: [
                "Диагностика с помощью современного оборудования",
                "Безболезненное лечение под местной анестезией",
                "Использование светоотверждаемых пломб",
                "Сохранение максимального объема здоровых тканей",
                "Гарантия на пломбы - 2 года"
            ],
            duration: "30-60 минут",
            anesthesia: "Местная"
        },
        2: {
            title: "Лечение пульпита",
            description: "Пульпит - воспаление зубного нерва (пульпы), которое требует немедленного лечения. Мы используем современные методы лечения, позволяющие сохранить зуб и избежать осложнений.",
            features: [
                "Точная диагностика состояния пульпы",
                "Механическая и медикаментозная обработка каналов",
                "Использование дентального микроскопа",
                "Герметичное пломбирование каналов",
                "Контроль качества лечения рентгеном"
            ],
            duration: "1-2 часа",
            anesthesia: "Местная"
        }
        // Добавьте остальные услуги по аналогии
    };

    infoBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const serviceId = this.getAttribute('data-service');
            showServiceDetails(serviceId);
        });
    });

    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    function showServiceDetails(serviceId) {
        const service = serviceDetails[serviceId] || {
            title: "Подробная информация",
            description: "Полное описание услуги, включая все детали процедуры, подготовку и рекомендации после лечения.",
            features: [
                "Профессиональная консультация",
                "Современное оборудование",
                "Квалифицированные специалисты",
                "Гарантия качества",
                "Индивидуальный подход"
            ],
            duration: "Зависит от сложности",
            anesthesia: "По показаниям"
        };

        modalBody.innerHTML = `
            <div class="service-details">
                <h2>${service.title}</h2>
                <p class="service-full-description">${service.description}</p>

                <div class="service-features">
                    <h3>Что включает услуга:</h3>
                    <ul>
                        ${service.features.map(feature => `<li>${feature}</li>`).join('')}
                    </ul>
                </div>

                <div class="service-info-grid">
                    <div class="info-item">
                        <strong>Продолжительность:</strong>
                        <span>${service.duration}</span>
                    </div>
                    <div class="info-item">
                        <strong>Анестезия:</strong>
                        <span>${service.anesthesia}</span>
                    </div>
                </div>

                <div class="modal-actions">
                    <a href="/entry/?service=${serviceId}" class="service-btn primary" style="display: block; text-align: center;">Записаться на прием</a>
                </div>
            </div>
        `;

        modal.style.display = 'block';
    }

    // Плавное появление карточек
    serviceCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});