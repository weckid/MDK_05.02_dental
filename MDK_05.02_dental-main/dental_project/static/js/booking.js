// booking.js - Система записи на прием
document.addEventListener('DOMContentLoaded', function() {
    const bookingModal = document.getElementById('bookingModal');
    const bookButtons = document.querySelectorAll('.book-appointment-btn');
    const closeButtons = document.querySelectorAll('.close-modal');
    const bookingCancel = document.querySelector('.booking-cancel');
    const bookingForm = document.getElementById('bookingForm');

    // Открытие модального окна записи
    bookButtons.forEach(button => {
        button.addEventListener('click', function() {
            const serviceId = this.getAttribute('data-service-id');
            const serviceName = this.getAttribute('data-service-name');
            const servicePrice = this.getAttribute('data-service-price');
            const serviceDescription = this.getAttribute('data-service-description');

            // Заполняем модальное окно данными услуги
            document.getElementById('modalServiceName').textContent = serviceName;
            document.getElementById('modalServiceDescription').textContent = serviceDescription;
            document.getElementById('modalServicePrice').textContent = servicePrice + ' ₽';
            document.getElementById('serviceId').value = serviceId;

            // Показываем модальное окно
            bookingModal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });
    });

    // Закрытие модального окна
    closeButtons.forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            bookingModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    });

    if (bookingCancel) {
        bookingCancel.addEventListener('click', function() {
            bookingModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    }

    // Закрытие при клике вне модального окна
    window.addEventListener('click', function(event) {
        if (event.target === bookingModal) {
            bookingModal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Валидация даты (нельзя выбрать прошедшие даты)
    const dateInput = document.getElementById('appointment_date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;

        // Запрещаем выходные
        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const dayOfWeek = selectedDate.getDay();

            if (dayOfWeek === 0 || dayOfWeek === 6) { // Воскресенье или суббота
                showNotification('Запись доступна только в рабочие дни (пн-пт)', 'warning');
                this.value = '';
            }
        });
    }

    // Показ уведомлений
    function showNotification(message, type = 'info') {
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : '⚠️'}</span>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(notification);

        // Анимация появления
        setTimeout(() => notification.classList.add('show'), 100);

        // Автоматическое удаление
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }

    // Добавляем стили для уведомлений
    const notificationStyles = `
        .notification {
            position: fixed;
            top: 100px;
            right: 20px;
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-left: 4px solid #3b82f6;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 10000;
            max-width: 350px;
        }
        .notification.show {
            transform: translateX(0);
        }
        .notification.success {
            border-left-color: #10b981;
        }
        .notification.error {
            border-left-color: #ef4444;
        }
        .notification.warning {
            border-left-color: #f59e0b;
        }
        .notification-content {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .notification-icon {
            font-size: 1.2rem;
        }
        .auth-required {
            text-align: center;
            padding: 2rem;
        }
        .auth-buttons-modal {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
        }
        .auth-buttons-modal .service-btn {
            min-width: 120px;
        }
    `;

    const styleSheet = document.createElement('style');
    styleSheet.textContent = notificationStyles;
    document.head.appendChild(styleSheet);
});
