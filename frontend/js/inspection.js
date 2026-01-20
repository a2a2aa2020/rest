// Inspection Form JavaScript

// Clear old results when starting new inspection
window.addEventListener('DOMContentLoaded', () => {
    sessionStorage.removeItem('inspectionResults');
});

let currentStep = 1;
const totalSteps = 5;

// Step to image ID mapping (without facade)
const stepImageMap = {
    2: 'ceilingImage',
    3: 'wallImage',
    4: 'floorImage',
    5: 'lightingImage'
};

function nextStep() {
    if (currentStep < totalSteps) {
        // Validate if current step requires an image
        if (stepImageMap[currentStep]) {
            const imageInput = document.getElementById(stepImageMap[currentStep]);
            if (!imageInput || !imageInput.files || !imageInput.files[0]) {
                alert('⚠️ الرجاء التقاط الصورة المطلوبة قبل المتابعة');
                // Highlight the camera placeholder
                const placeholder = imageInput.parentElement.querySelector('.camera-placeholder');
                if (placeholder) {
                    placeholder.style.border = '3px solid #dc3545';
                    placeholder.style.animation = 'shake 0.5s';
                    setTimeout(() => {
                        placeholder.style.border = '';
                        placeholder.style.animation = '';
                    }, 2000);
                }
                return; // Don't proceed to next step
            }
        }

        // Hide current step
        document.getElementById(`step${currentStep}`).style.display = 'none';

        // Update step indicator
        document.querySelectorAll('.step-dot')[currentStep - 1].classList.remove('active');
        document.querySelectorAll('.step-dot')[currentStep - 1].classList.add('completed');

        // Show next step
        currentStep++;
        document.getElementById(`step${currentStep}`).style.display = 'block';
        document.querySelectorAll('.step-dot')[currentStep - 1].classList.add('active');

        // Scroll to top
        window.scrollTo(0, 0);
    }
}

function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.innerHTML = `
                <img src="${e.target.result}" class="image-preview" alt="معاينة الصورة">
                <div class="text-center mt-2">
                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="removeImage('${input.id}', '${previewId}')">
                        إزالة الصورة
                    </button>
                </div>
            `;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function removeImage(inputId, previewId) {
    document.getElementById(inputId).value = '';
    document.getElementById(previewId).innerHTML = '';
}

async function submitInspection() {
    // Validate all images are uploaded
    const requiredImages = ['ceilingImage', 'wallImage', 'floorImage', 'lightingImage'];
    for (const imageId of requiredImages) {
        if (!document.getElementById(imageId).files[0]) {
            alert('الرجاء رفع جميع الصور المطلوبة');
            return;
        }
    }

    // Show loading modal
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();

    // Simulate progress
    simulateProgress();

    // Prepare form data
    const formData = new FormData();
    formData.append('restaurant_name', document.getElementById('restaurantName').value);
    formData.append('commercial_register', document.getElementById('commercialRegister').value);
    // Append images (4 images now - no facade)
    formData.append('ceiling_image', document.getElementById('ceilingImage').files[0]);
    formData.append('wall_image', document.getElementById('wallImage').files[0]);
    formData.append('floor_general_image', document.getElementById('floorImage').files[0]);
    formData.append('floor_prep_image', document.getElementById('floorImage').files[0]); // Same for POC
    formData.append('lighting_image', document.getElementById('lightingImage').files[0]);


    try {
        // Add timeout to prevent infinite loading (3 minutes for AI processing)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 300 seconds (5 minutes) timeout

        const response = await fetch('https://restaurant-inspection-api.onrender.com/api/analyze', {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error('فشل الفحص');
        }

        const results = await response.json();

        // Store results in sessionStorage
        sessionStorage.setItem('inspectionResults', JSON.stringify(results));

        // Redirect to results page
        setTimeout(() => {
            window.location.href = 'results.html';
        }, 2000);

    } catch (error) {
        console.error('Error:', error);
        loadingModal.hide();

        // Better error messages
        if (error.name === 'AbortError') {
            alert('⏱️ استغرق التحليل أكثر من 3 دقائق.\n\n💡 نصيحة: في أول استخدام، الخدمة قد تحتاج وقتاً للتشغيل.\nالرجاء المحاولة مرة أخرى الآن - سيكون أسرع!');
        } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            alert('❌ فشل الاتصال بالخادم.\n\nالرجاء التحقق من اتصال الإنترنت والمحاولة مرة أخرى.');
        } else {
            alert('حدث خطأ أثناء الفحص. الرجاء المحاولة مرة أخرى.');
        }
    }
}

function simulateProgress() {
    const progressBar = document.getElementById('progressBar');
    let progress = 0;

    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) {
            progress = 100;
            clearInterval(interval);
        }
        progressBar.style.width = `${progress}%`;
    }, 500);
}

