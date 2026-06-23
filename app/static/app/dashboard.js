// Sidebar toggle
const sidebar = document.getElementById('sidebar');
const menuBtn = document.getElementById('menuBtn');
const overlay = document.getElementById('overlay');

menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('show');
});
overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
});

// Set last login date
const loginDate = document.getElementById('loginDate');
if (loginDate) {
    const now = new Date();
    loginDate.textContent = now.toISOString().replace('T', ' ').slice(0, 19);
}

// Daily Stats chart
(function () {
    const dataEl = document.getElementById('chartData');
    const canvas = document.getElementById('statsChart');
    if (!dataEl || !canvas) return;

    let chartData;
    try {
        chartData = JSON.parse(dataEl.textContent);
    } catch (e) {
        console.error('Chart data parse error:', e);
        return;
    }

    // Destroy existing chart instance if any to prevent infinite loop
    const existing = Chart.getChart(canvas);
    if (existing) existing.destroy();

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: 'Wire Transfer',
                    data: chartData.wire,
                    backgroundColor: 'rgba(0, 91, 230, 0.78)',
                    borderRadius: 6,
                    borderSkipped: false,
                },
                {
                    label: 'Domestic Transfer',
                    data: chartData.domestic,
                    backgroundColor: 'rgba(245, 158, 11, 0.78)',
                    borderRadius: 6,
                    borderSkipped: false,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 600 },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const val = context.parsed.y;
                            if (val >= 1000000) return ` ${context.dataset.label}: ${(val / 1000000).toFixed(2)}M`;
                            if (val >= 1000) return ` ${context.dataset.label}: ${(val / 1000).toFixed(1)}k`;
                            return ` ${context.dataset.label}: ${val.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Poppins', size: 11 }, color: '#64748b' }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.05)' },
                    ticks: {
                        font: { family: 'Poppins', size: 11 },
                        color: '#64748b',
                        callback: v => {
                            if (v >= 1000000) return (v / 1000000).toFixed(1) + 'M';
                            if (v >= 1000) return (v / 1000).toFixed(0) + 'k';
                            return v;
                        }
                    }
                }
            }
        }
    });
})();