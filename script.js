// Modal functions
function openModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
}

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// API URL для отправки заявок
// Сервер задеплоен на Render
const API_URL = 'https://pybot-ai-website.onrender.com/api/submit';

// Form submission handler
async function handleSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    
    // Basic validation
    if (!name || !phone) {
        alert('Пожалуйста, заполните все поля');
        return;
    }
    
    // Phone validation (basic)
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    if (!phoneRegex.test(phone)) {
        alert('Пожалуйста, введите корректный номер телефона');
        return;
    }
    
    // Показываем индикатор загрузки
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = 'Отправка...';
    
    try {
        console.log('📤 Отправка заявки на сервер:', API_URL);
        console.log('📋 Данные:', { name, phone });
        
        // Отправляем данные на сервер
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, phone })
        });
        
        console.log('📥 Ответ сервера:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Ошибка сервера:', errorText);
            throw new Error(`Ошибка сервера: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('✅ Данные от сервера:', data);
        
        if (data.success) {
            // Показываем сообщение об успехе
            const modalContent = document.querySelector('.modal-content');
            modalContent.innerHTML = `
                <span class="close" onclick="closeModal()">&times;</span>
                <div style="text-align: center; padding: 20px 0;">
                    <div style="font-size: 4rem; margin-bottom: 20px;">✓</div>
                    <h2 style="color: #10b981; margin-bottom: 16px;">Спасибо за заявку!</h2>
                    <p style="color: #64748b; margin-bottom: 24px;">
                        Мы получили вашу заявку и свяжемся с вами в течение 24 часов.
                    </p>
                    <button class="cta-button" onclick="closeModal()">Закрыть</button>
                </div>
            `;
            
            // Reset form
            form.reset();
            
            console.log('Заявка успешно отправлена в Telegram');
        } else {
            throw new Error(data.error || 'Ошибка при отправке заявки');
        }
    } catch (error) {
        console.error('❌ Ошибка отправки заявки:', error);
        console.error('   Детали:', error.message);
        console.error('   URL:', API_URL);
        
        // Показываем сообщение об ошибке с деталями
        const modalContent = document.querySelector('.modal-content');
        const errorMessage = error.message.includes('CORS') || error.message.includes('Failed to fetch')
            ? 'Проблема с подключением к серверу. Проверьте консоль браузера (F12) для деталей.'
            : error.message;
        
        modalContent.innerHTML = `
            <span class="close" onclick="closeModal()">&times;</span>
            <div style="text-align: center; padding: 20px 0;">
                <div style="font-size: 4rem; margin-bottom: 20px;">⚠️</div>
                <h2 style="color: #f59e0b; margin-bottom: 16px;">Ошибка отправки</h2>
                <p style="color: #64748b; margin-bottom: 16px;">
                    ${errorMessage}
                </p>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px;">
                    Откройте консоль браузера (F12) для подробностей
                </p>
                <button class="cta-button" onclick="closeModal()">Закрыть</button>
            </div>
        `;
        
        form.reset();
    } finally {
        // Восстанавливаем кнопку
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.service-card, .benefit-item, .problem-item');
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

