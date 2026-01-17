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
        // Demo results for testing
        results = {
            inspection_id: 'INS_20260117_120000',
            restaurant_name: 'مطعم النخيل',
            commercial_register: '1010567890',
            overall_status: 'compliant',
            overall_score: 95.3,
            timestamp: new Date().toISOString(),
            criteria: [
                {
                    criterion_id: 1,
                    criterion_name: 'الأسلاك والأنابيب الظاهرة',
                    status: 'compliant',
                    score: 96,
                    confidence: 0.92,
                    details: {
                        ceiling: { has_exposed_wires: false, description: 'لا توجد أسلاك ظاهرة' },
                        wall: { has_exposed_wires: false, description: 'لا توجد أسلاك ظاهرة' },
                        floor_general: { has_exposed_wires: false, description: 'لا توجد أسلاك ظاهرة' }
                    }
                },
                {
                    criterion_id: 2,
                    criterion_name: 'وحدات التكييف على الواجهة',
                    status: 'compliant',
                    score: 98,
                    confidence: 0.95,
                    details: {
                        facade: { has_ac_units: false, description: 'لا توجد وحدات تكييف ظاهرة' }
                    }
                },
                {
                    criterion_id: 3,
                    criterion_name: 'الأرضيات بدون فواصل',
                    status: 'compliant',
                    score: 92,
                    confidence: 0.88,
                    details: {
                        floor: { has_joints: false, description: 'الأرضية موحدة بدون فواصل' }
                    }
                },
                {
                    criterion_id: 4,
                    criterion_name: 'كفاية الإضاءة',
                    status: 'compliant',
                    score: 95,
                    confidence: 0.90,
                    details: {
                        lighting: { is_adequate: true, description: 'مستوى الإضاءة جيد (85%)' }
                    }
                }
            ],
            pdf_report: '/reports/inspection_report_INS_20260117_120000.pdf'
        };
    } else {
        results = JSON.parse(resultsData);
    }

    displayResults();
}

function displayResults() {
    // Overall summary
    const statusMap = {
        'compliant': { text: 'مستوفي للمعايير', icon: '🎉', class: 'text-success' },
        'needs_improvement': { text: 'يحتاج تحسينات', icon: '⚠️', class: 'text-warning' },
        'non_compliant': { text: 'غير مستوفي', icon: '❌', class: 'text-danger' }
    };

    const status = statusMap[results.overall_status] || statusMap['non_compliant'];

    document.getElementById('resultSummary').innerHTML = `
        <div class="result-icon">${status.icon}</div>
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
    const statusColors = {
        'compliant': 'success',
        'needs_improvement': 'warning',
        'non_compliant': 'danger'
    };

    const statusIcons = {
        'compliant': '✓',
        'needs_improvement': '⚠',
        'non_compliant': '✗'
    };

    const card = document.createElement('div');
    card.className = 'criterion-card';

    card.innerHTML = `
        <div class="criterion-header">
            <div class="criterion-name">${criterion.criterion_name}</div>
            <div class="criterion-score">
                <span class="badge bg-${statusColors[criterion.status]}" style="font-size: 1.2rem; padding: 0.75rem 1.25rem;">
                    ${statusIcons[criterion.status]} ${criterion.score}/100
                </span>
            </div>
        </div>
        <div class="progress mb-3" style="height: 8px;">
            <div class="progress-bar bg-${statusColors[criterion.status]}" style="width: ${criterion.score}%"></div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="info-label">الحالة</div>
                <div class="info-value">
                    <span class="status-badge status-${criterion.status}">
                        ${statusIcons[criterion.status]} ${getStatusText(criterion.status)}
                    </span>
                </div>
            </div>
            <div class="col-md-6">
                <div class="info-label">دقة التحليل</div>
                <div class="info-value">${(criterion.confidence * 100).toFixed(0)}%</div>
            </div>
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
