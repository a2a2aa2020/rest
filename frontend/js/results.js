// Results Page JavaScript

// Load results from sessionStorage
let results = null;

window.addEventListener('DOMContentLoaded', () => {
    loadResults();
    setupEventListeners();
});

function loadResults() {
    const resultsData = sessionStorage.getItem('inspectionResults');

    if (!resultsData) {
        // No results found - redirect to home
        alert('⚠️ لا توجد نتائج فحص.\n\nالرجاء إجراء فحص جديد.');
        window.location.href = 'index.html';
        return;
    }

    results = JSON.parse(resultsData);
    displayResults();
}

function displayResults() {
    // Overall summary
    const statusMap = {
        'compliant': { text: 'مستوفي للمعايير', class: 'text-success' },
        'needs_improvement': { text: 'يحتاج تحسينات', class: 'text-warning' },
        'non_compliant': { text: 'غير مستوفي', class: 'text-danger' }
    };

    const status = statusMap[results.overall_status] || statusMap['non_compliant'];

    document.getElementById('resultSummary').innerHTML = `
        <div class="result-title ${status.class}">${status.text}</div>
        <div class="result-score mb-3">${results.overall_score.toFixed(1)}/100</div>
        <p class="text-secondary">${getStatusMessage(results.overall_status)}</p>
    `;

    // Restaurant info
    document.getElementById('restaurantName').textContent = results.restaurant_name;
    document.getElementById('commercialRegister').textContent = results.commercial_register;
    document.getElementById('inspectionId').textContent = results.inspection_id;

    // Criteria results
    const criteriaContainer = document.getElementById('criteriaResults');
    criteriaContainer.innerHTML = '';

    results.criteria.forEach(criterion => {
        const criterionCard = createCriterionCard(criterion);
        criteriaContainer.appendChild(criterionCard);
    });
}

function createCriterionCard(criterion) {
    const statusData = {
        'compliant': {
            icon: '✓',
            text: 'مستوفي',
            color: '#2E7D32',
            borderColor: '#4CAF50'
        },
        'needs_improvement': {
            icon: '!',
            text: 'يحتاج تحسين',
            color: '#F57F17',
            borderColor: '#FFC107'
        },
        'non_compliant': {
            icon: '✗',
            text: 'غير مستوفي',
            color: '#C62828',
            borderColor: '#F44336'
        }
    };

    const status = statusData[criterion.status] || statusData['non_compliant'];

    const card = document.createElement('div');
    card.className = 'criterion-card';

    card.innerHTML = `
        <div class="criterion-header-new">
            <div class="criterion-name-large">${criterion.criterion_name}</div>
        </div>
        <div class="status-icon-container">
            <div class="status-circle" style="border-color: ${status.borderColor};">
                <div class="status-icon" style="color: ${status.color};">${status.icon}</div>
            </div>
            <div class="status-text" style="color: ${status.color};">${status.text}</div>
        </div>
        ${createDetailsSection(criterion.details)}
    `;

    return card;
}

function createDetailsSection(details) {
    let html = '<div class="mt-3"><div class="info-label">التفاصيل:</div><ul class="list-unstyled mt-2">';

    for (const [key, value] of Object.entries(details)) {
        if (value.description) {
            html += `<li class="mb-1">• ${value.description}</li>`;
        }
    }

    html += '</ul></div>';
    return html;
}

function getStatusText(status) {
    const map = {
        'compliant': 'مستوفي',
        'needs_improvement': 'يحتاج تحسين',
        'non_compliant': 'غير مستوفي'
    };
    return map[status] || 'غير محدد';
}

function getStatusMessage(status) {
    const messages = {
        'compliant': 'تهانينا! المنشأة مستوفية لجميع المعايير المطلوبة',
        'needs_improvement': 'المنشأة بحاجة إلى بعض التحسينات البسيطة',
        'non_compliant': 'يرجى معالجة النقاط غير المستوفاة قبل إعادة الفحص'
    };
    return messages[status] || '';
}

function setupEventListeners() {
    // Download PDF
    document.getElementById('downloadPDFBtn').addEventListener('click', () => {
        if (results && results.pdf_report) {
            window.open(`https://restaurant-inspection-api.onrender.com${results.pdf_report}`, '_blank');
        } else {
            alert('التقرير غير متوفر حالياً');
        }
    });

    // Share with Ministry
    document.getElementById('shareBtn').addEventListener('click', () => {
        const modal = new bootstrap.Modal(document.getElementById('successModal'));
        modal.show();
    });
}
